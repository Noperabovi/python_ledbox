import pyaudio
import audioop
import struct

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 2 * 1024
# INPUT_BLOCK_TIME = 0.05
# INPUT_FRAMES_PER_BLOCK = int(RATE*INPUT_BLOCK_TIME)


threshold = 15
min_silent = 5
min_loud = 2
max_loud = 5


class TapTester(object):
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        self.stream = self.open_mic_stream()
        self.loud = 0
        self.silent_before = 0
        self.silent_after = 0

    def stop(self):
        self.stream.close()


    def open_mic_stream( self ):
        self.defaultDevice = self.pa.get_default_input_device_info()
        self.channels = int(self.defaultDevice['maxInputChannels'])
        self.rate = int(self.defaultDevice['defaultSampleRate'])

        stream = self.pa.open(  format = FORMAT,
                                #  channels = self.channels,
                                #  rate = self.rate,
                                channels = CHANNELS,
                                rate = RATE,
                                input = True,
                                frames_per_buffer = CHUNK)

        return stream

    def listen(self):
        try:
            block = self.stream.read(CHUNK)
        except e:
            # dammit.
            self.errorcount += 1
            print( "(%d) Error recording: %s"%(self.errorcount,e) )
            self.noisycount = 1
            return

        amplitude = audioop.rms(block, 2)
        # print(amplitude)

        # print(struct.unpack(str(2*CHUNK) + 'B', block))

        # threshold = 15
        # min_silent = 5
        # min_loud = 2
        # max_loud = 5

        # loud = 0
        # silent_before = 0
        # silent_after = 0

        if amplitude < threshold:

            if self.loud == 0:
                self.silent_before += 1
            else:
                self.silent_after += 1

                # not enough silent blocks before loud block or wrong number of loud blocks
                if self.silent_before < min_silent or self.loud < min_loud or self.loud > max_loud:
                    self.silent_before = 1
                    self.loud = 0

                # enough silent blocks after clap
                elif self.silent_after >= min_silent:
                    print("clap!")
                    self.loud = 0
                    self.silent_before = self.silent_after

        else:
            self.loud += 1
            self.silent_after = 0


if __name__ == "__main__":
    try:
        tt = TapTester()

        while True:
            tt.listen()

    except Exception as e:
        print(e)
