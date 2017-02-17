# _*_ coding: utf-8 _*_

import sys

current_id = None
current_md5 = None
current_gender = None
current_age = None
current_job = None
current_tags = None

for line in sys.stdin:
    frags = line.strip().split("\t")
    device_id, device_md5, device_content = frags[0], frags[1], frags[2:]

    if current_id and current_id != device_id:
        temp = "\t".join([current_id, current_md5,
                          "\t".join(current_gender[1:3] if current_gender else ["unknown"]*2),
                          "\t".join(current_age[1:3] if current_age else ["unknown"]*2),
                          "\t".join(current_tags[1:3] if current_tags else ["unknown"] * 2),
                          "unknown", current_job[1] if current_job else "unknown"])
        assert len(temp.split("\t")) == 10, str(temp.split("\t"))
        print(temp.strip())

        current_id = device_id
        current_md5 = device_md5
        current_tags = device_content if device_content[0] == "tags" else None
        current_gender = device_content if device_content[0] == "gender" else None
        current_age = device_content if device_content[0] == "age" else None
        current_job = device_content if device_content[0] == "job" else None
    else:
        current_id = device_id
        current_md5 = device_md5
        if device_content[0] == "tags":
            current_tags = device_content
        if device_content[0] == "gender":
            current_gender = device_content
        if device_content[0] == "age":
            current_age = device_content
        if device_content[0] == "job":
            current_job = device_content

temp = "\t".join([current_id, current_md5,
                  "\t".join(current_gender[1:3] if current_gender else ["unknown"]*2),
                  "\t".join(current_age[1:3] if current_age else ["unknown"]*2),
                  "\t".join(current_tags[1:3] if current_tags else ["unknown"] * 2),
                  "unknown", current_job[1] if current_job else "unknown"])
assert len(temp.split("\t")) == 10, str(temp.split("\t"))
print(temp.strip())
