# RHUL MPC Challenges

## How to deploy

To deploy in local the challenges, after cloning the repository, follow this step:

1. Install [Docker](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
2. Open the project’s root folder in your terminal.
3. Run `docker-compose up --build` in the terminal.

Once the build is complete, the infrastructure will be up and accessible via `localhost`.

## How to connect

### Offline Challenges

These challenges are missing the `Dockerfile` and `run.sh` files in their folders. So, to test them, the public files (`files/`) are sufficient.

### Online Challenges

To get the flag, you not only need to look at the public files, but also connect via server. Every challenge is associated to a port, which you can retrieve by looking at the `docker-compose.yml` in the root directory.

To connect locally (after deployment), you can use netcat and run in the terminal:

```bash
nc localhost <port>
```

For example, for `challenge 00/00`, in the `docker-compose.yml` we can read
```yaml
rhul-00-00:
    build:
      context: ./challenges/00-introduction/00-outsourced-computation
    container_name: rhul_00_00
    restart: unless-stopped
    tty: true
    ports:
      - "1337:1337"
    read_only: true
```

the port associated is 1337. To connect, simply run:
```bash
nc localhost 1337
```