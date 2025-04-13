#!/usr/bin/env python3
import asyncio

SERVER_IP = '0.0.0.0'  # Ziel IP
SERVER_PORT = 443 # Ziel Port
TARGET_CONNECTIONS = 64512  # Gewünschte Anzahl von Verbindungen

connections = []

async def create_connection(index):
    try:
        reader, writer = await asyncio.open_connection(SERVER_IP, SERVER_PORT)
        connections.append(writer)
        if index % 1000 == 0:
            print(f"Verbindung {index} hergestellt")
    except Exception as e:
        print(f"Fehler bei Verbindung {index}: {e}")

async def main():
    tasks = []
    for i in range(1, TARGET_CONNECTIONS + 1):
        task = asyncio.create_task(create_connection(i))
        tasks.append(task)
        if i % 1000 == 0:
            await asyncio.sleep(0.1)  # Kurze Pause, um Überlastung zu vermeiden

    await asyncio.gather(*tasks)
    print(f"Erstellt {len(connections)} Verbindungen.")

    # Halte die Verbindungen offen
    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("Verbindungen werden geschlossen.")
        for writer in connections:
            writer.close()
            await writer.wait_closed()

if __name__ == "__main__":
    asyncio.run(main())
    
    
    
# ulimit -n 200000   (unbedingt setzen)
