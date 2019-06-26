from modelarts.session import Session

class Bucket:

    def __init__(self):
        session = Session()
        self._session = session
        self._buckets_client = session.get_obs_client()

if __name__ == "__main__":
    bucket = Bucket()


