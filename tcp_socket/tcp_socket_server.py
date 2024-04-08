import socket
import logging
import threading

# 연결된 모든 클라이언트를 저장하는 리스트
connected_clients = []

# 로그 파일 설정
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 클라이언트와의 통신을 처리하는 함수
def handle_client_connection(conn, addr):
    with conn:
        print(f"연결된 소켓은 {addr}")

        # 클라이언트 연결을 리스트에 추가
        connected_clients.append(conn)

        while True:
            try:
                # 클라이언트로부터 데이터를 받습니다. 한 번에 최대 1024바이트를 읽을 수 있습니다.
                data = conn.recv(1024)
                if not data:
                    break

                # 받은 데이터를 로그 파일에 기록
                logging.info(f"Received coordinates: {data.decode()}")

                # 받은 데이터를 그대로 클라이언트에게 전송
                 # 받은 데이터를 모든 클라이언트에게 전송
                for client in connected_clients:
                    client.sendall(data)

                #conn.sendall(data)
            except Exception as e:
                logging.error(f"An error occurred: {str(e)}")
                break

# TCP 서버를 시작하는 함수입니다.
def start_server(host='0.0.0.0', port=6521):
    # socket 객체를 생성합니다. AF_INET은 IPv4를 사용하겠다는 의미이고, SOCK_STREAM은 TCP를 사용하겠다는 의미입니다.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        # 생성한 소켓을 주어진 호스트와 포트에 바인드(연결)합니다. 이는 서버가 해당 주소에서 클라이언트의 연결을 기다리게 합니다.
        socket_server.bind((host, port))
        # 소켓이 클라이언트의 연결을 기다리도록 설정합니다. 이 메서드는 소켓을 "리스닝" 상태로 만듭니다.
        socket_server.listen()
        print(f"서버가 연결되었습니다. {host}:{port}")

        while True:
            # 클라이언트로부터 연결이 수립되면, accept 메서드는 연결된 클라이언트의 소켓 객체와 주소를 반환합니다.
            conn, addr = socket_server.accept()
            # 새로운 스레드를 생성하여 클라이언트와의 통신을 처리합니다.
            client_thread = threading.Thread(target=handle_client_connection, args=(conn, addr))
            client_thread.start()

# 이 스크립트가 직접 실행되었을 때만 start_server 함수를 호출합니다.
if __name__ == "__main__":
    start_server()