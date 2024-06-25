import argparse
import dataclasses
import os
import subprocess
from os import path

project_root = path.abspath(path.join(__file__, "../.."))
gcloud_project_id = "agent-connect-427518"


@dataclasses.dataclass
class BuildInfo:
    is_prod: bool
    is_full_collect: bool
    should_migrate_db: bool
    migration_db_url: str

    def validate(self):
        if self.should_migrate_db and len(self.migration_db_url) < 4:
            raise Exception("Canceling deploy since db migration was requested but no db URL is specified")
        if not self.is_prod and self.should_migrate_db and "prod" in self.migration_db_url:
            raise Exception("The word prod is in the db url and this is a staging build")

    def get_bucket(self) -> str:
        if self.is_prod:
            return "agent-connect-prod"
        raise Exception()

    def get_docker_repo(self) -> str:
        if self.is_prod:
            return "agent-connect-prod"
        raise Exception()

    def get_cloud_run_name(self) -> str:
        if self.is_prod:
            return "agent-connect-prod"
        raise Exception()


def docker_build(info: BuildInfo):
    print("Building container")
    subprocess.run(["docker", "buildx", "build", "--target", "app", "--platform", "linux/amd64", "-t", f"us-west1-docker.pkg.dev/agent-connect-427518/{info.get_docker_repo()}/server:server", "."], cwd=project_root)
    subprocess.run(["docker", "push", f"us-west1-docker.pkg.dev/agent-connect-427518/{info.get_docker_repo()}/server:server"], cwd=project_root)


def deploy_run_run(info: BuildInfo):
    image_name = f"us-west1-docker.pkg.dev/agent-connect-427518/{info.get_docker_repo()}/server:server"
    subprocess.run(["gcloud", "run", "deploy", info.get_cloud_run_name(), "--image", image_name, "--region", "us-west1", "--allow-unauthenticated", "--project", gcloud_project_id], cwd=project_root)


def collect_static(info: BuildInfo):
    print("Uploading static assets")
    os.environ['ENV'] = "COLLECT_STATIC"
    os.environ['GS_BUCKET_NAME'] = info.get_bucket()

    ingore_list = ["-i", "DEBUG"]
    if info.is_full_collect is False:
        ingore_list = ["-i", "DEBUG", "-i", "admin"]

    cmd = ["python", "manage.py", "collectstatic", "--noinput"]
    subprocess.run(cmd + ingore_list, cwd=project_root)
    os.environ['ENV'] = ""


def migrate_db(info: BuildInfo):
    if not info.should_migrate_db:  # extra safe!
        return
    os.environ['ENV'] = "LOCAL"
    os.environ['DB_URL'] = info.migration_db_url
    cmd = ["python", "manage.py", "migrate"]
    subprocess.run(cmd, cwd=project_root)


parser = argparse.ArgumentParser(
                    prog='Deploy script',
                    description='Handles deploying')


parser.add_argument('-t', '--type', action='store', default="STAGING", choices=["STAGING", "PROD"])
parser.add_argument('-fc', '--full_collect', action='store_true')
parser.add_argument('-m', '--migrate', action='store_true')
parser.add_argument('-db', '--db_url', action='store')


if __name__ == "__main__":
    args = parser.parse_args()

    info = BuildInfo(
        is_prod=args.type.upper() == "PROD",
        is_full_collect=args.full_collect,
        migration_db_url=args.db_url,
        should_migrate_db=args.migrate,
    )

    info.validate()

    collect_static(info)
    docker_build(info)

    if info.should_migrate_db:
        migrate_db(info)

    deploy_run_run(info)



