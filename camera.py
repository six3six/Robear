import picamera
import pyshine as ps 


def main():
    StreamProps = ps.StreamProps
    address = ('0.0.0.0', 9000) 
    StreamProps.set_Mode(StreamProps, 'picamera')
    with picamera.PiCamera(resolution='640x480', framerate=30) as camera:
        output = ps.StreamOut()
        StreamProps.set_Output(StreamProps, output)
        camera.start_recording(output, format='mjpeg')
        try:
            server = ps.Streamer(address, StreamProps)
            print('Server started at', 'http://' +
                  address[0]+':'+str(address[1]))
            server.serve_forever()
        finally:
            camera.stop_recording()


if __name__ == '__main__':
    main()
