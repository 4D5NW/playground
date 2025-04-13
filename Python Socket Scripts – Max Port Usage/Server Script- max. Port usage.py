#!/usr/bin/env python3
import asyncio
import uvloop
import multiprocessing
import os
import socket
from multiprocessing import Value, Lock

HOST = '0.0.0.0' # IP
PORT = 443  # Portwahl
MAX_CONNECTIONS = 100000  # Anzahl gleichzeitiger Verbindungen

# Gemeinsame Variable zur Zählung der Verbindungen zwischen Prozessen
connection_count = Value('i', 0)
count_lock = Lock()

async def handle_client(reader, writer):
    global connection_count
    addr = writer.get_extra_info('peername')

    with count_lock:
        connection_count.value += 1

    try:
        while True:
            data = await reader.read(1024)
            if not data:
                break
            # Hier optional Daten verarbeiten
    except Exception as e:
        pass
    finally:
        writer.close()
        await writer.wait_closed()
        with count_lock:
            connection_count.value -= 1

async def log_connections():
    while True:
        with count_lock:
            current = connection_count.value
        print(f"Aktive Verbindungen: {current}")
        await asyncio.sleep(10)  # Alle 10 Sekunden ausgeben

async def main(server_socket):
    server = await asyncio.start_server(handle_client, sock=server_socket)
    addr = server.sockets[0].getsockname()
    print(f"Prozess {os.getpid()}: Server lauscht auf {addr}")

    # Starte das Logging-Task
    asyncio.create_task(log_connections())

    async with server:
        await server.serve_forever()

def start_server():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    # Erstelle das Socket mit SO_REUSEPORT
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    sock.bind((HOST, PORT))
    sock.listen()
    sock.setblocking(False)
    asyncio.run(main(sock))

if __name__ == '__main__':
    cpu_count = multiprocessing.cpu_count()
    print(f"Starte {cpu_count} Prozesse für den Server.")
    processes = []
    for _ in range(cpu_count):
        p = multiprocessing.Process(target=start_server)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()
        
        
# ulimit -n 200000
# source myenv/bin/activate
