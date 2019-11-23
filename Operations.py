from Architecture import Pipeline


class Operations(object):

    def __init__(self):

        pipeline = Pipeline()

        self.fetch = pipeline.fetch
        self.decode = pipeline.decode
        self.execute = pipeline.execute
        self.write_back = pipeline.write_back

        self.fetch_busy = pipeline.fetch_busy
        self.decode_busy = pipeline.decode_busy
        self.execute_busy = pipeline.execute_busy
        self.write_back_busy = pipeline.write_back_busy

    def load(self):

        if not self.fetch_busy:
            self.fetch_busy = True
            self.fetch += 1
        if not self.decode_busy:
            self.decode += self.fetch + 1
        if not self.execute_busy:
            self.execute += self.decode + int(self.config[0]['Main memory']) + 1
        if not self.write_back:
            self.write_back += self.execute + 1
r = Operations()
r.load()