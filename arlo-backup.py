import pdb
from arlo import Arlo
from datetime import timedelta, date
from dateutil import tz
import datetime
import argparse
from retry import retry

ap = argparse.ArgumentParser()
ap.add_argument('-u', '--username', required=True, help='Username of Arlo account')
ap.add_argument('-p', '--password', required=True, help='Password of Arlo account')
ap.add_argument('-d', '--date', required=False, default=date.today().strftime("%Y.%m.%d"),
                help='Date to start downloading videos from. Format YYYYMMDD. Default today.')
ap.add_argument('-n', '--num_days', required=False, default=0,
                help='Days in the past to download videos for. Default 0 (downloads only for the current day).')
args = vars(ap.parse_args())


# Convert the array of devices into a dict that allows easier access to
# the information needed per camera via the device id
def make_device_map(lst):
    res_dct = {lst[i].get('deviceId'): lst[i] for i in range(0, len(lst), 1)}
    return res_dct


def format_millis_to_local_datetime(datetime_millis, to_zone_name):
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz(to_zone_name)
    # Tell the datetime object that it's in UTC time zone since datetime objects are 'naive' by default
    record_utc_time = datetime.datetime.utcfromtimestamp(datetime_millis).replace(tzinfo=from_zone)
    record_local_time = record_utc_time.astimezone(to_zone)
    return record_local_time.strftime('%Y-%m-%d_%H-%M-%S')


# Wrap all Arlo calls in a retry to avoid false failures due to a single bad api request

@retry(tries=3, delay=2)
def get_library(start, end):
    return arlo.GetLibrary(start, end)


@retry(tries=3, delay=2)
def get_devices(device_type):
    return arlo.GetDevices(device_type)


# Get video as a chunked stream; this function returns a generator.
# More memory efficient
# Higher delay due to the higher bandwidth
@retry(tries=3, delay=4)
def download_video(recording, video_filename):
    stream = arlo.StreamRecording(recording['presignedContentUrl'])
    # Note: /videos needs to exist in the local directory that this script is being run in.
    with open('videos/' + video_filename, 'wb') as f:
        for chunk in stream:
            f.write(chunk)
        f.close()
    return None


try:
    arlo = Arlo(args["username"], args["password"])
    print(date.today())
    end = args["date"]  # 'Start'
    start = (datetime.datetime.strptime(end, '%Y.%m.%d').date() - timedelta(days=args["num_days"])).strftime("%Y%m%d")

    print('Starting download of videos from: {}'.format(str(start)))
    print('Ending download of videos at: {}'.format(str(end)))

    # Get all of the recordings for a date range.
    library = get_library(start, end)

    videos_total = len(library)
    videos_success = 0
    videos_failure = 0

    pdb.set_trace()
    # Arlo breaks up video doorbells from cameras so we recombine them
    devices = get_devices('camera') + get_devices('doorbell')
    device_map = make_device_map(devices)

    # Iterate through the recordings in the library.
    for recording in library:
        recording_camera = device_map.get(recording.get('deviceId'))

        # Get the event that triggered the recording
        if recording.get('objCategory') is None:
            trigger = recording.get('reason')  # basic motion or sound
        else:
            trigger = recording.get('objCategory')  # person/animal/vehicle classification

        # Other file name attributes
        device_name = recording_camera.get('deviceName').replace(" ", "_")
        recording_time = format_millis_to_local_datetime(int(recording['name']) // 1000, recording['timeZone'])
        video_filename = device_name + '_' + trigger + '_' + recording_time + '.mp4'

        print('Downloading video {} from {}.'.format(video_filename, recording['createdDate']))

        try:
            download_video(recording, video_filename)
            print('Complete download video {} from {}.'.format(video_filename, recording['createdDate']))
            videos_success += 1
        except Exception as e:
            print('Failed to download video {}. Error: {}.'.format(video_filename, str(e)))
            videos_failure += 1

    print('Batch download of videos completed.')
    print('Total videos: {}'.format(str(videos_total)))
    print('Success: {}'.format(str(videos_success)))
    print('Failed: {}'.format(str(videos_failure)))

except Exception as e:
    print(e)
    exit(1)
