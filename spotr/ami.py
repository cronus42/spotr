from typing import Any


def get_by_tag(client: Any, tag: str) -> str:
    response = client.describe_images(Filters=[{"Name": "tag:project", "Values": [tag]}])
    images = response["Images"]
    if len(images) == 0:
        raise RuntimeError(f"No saved images with tag: '{tag}'")
    return images[0]["ImageId"]
