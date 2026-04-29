import os
import json
import subprocess
from pathlib import Path

# Mapping your IDs to your Repos
REPO_MAP = {
    # repo1: gen 3,6
    1484896149713457213: "dmkr48/gen3-6", #gita gen6

    1484896111696154674: "dmkr48/gen7", #christy gen7
    1484896125243887791: "dmkr48/gen", #eli gen7
    1484896166289342536: "dmkr48/gen7", #jessi gen7
    1484896202196521111: "dmkr48/gen7", #muthe gen7
    1484896206223048799: "dmkr48/gen7", #olla gen7
    1484896141614121101: "dmkr48/gen7", #freya gen7

    1484896138522918932: "dmkr48/gen8", #fiony gen8
    1484896185662836807: "dmkr48/gen8", #lulu gen8
    1484896211289899130: "dmkr48/gen8", #oniel gen8

    1484896162787102720: "dmkr48/gen9", #indah gen9
    1484896177127424111: "dmkr48/gen9", #kathrina gen9
    1484896193719828651: "dmkr48/gen9", #marsha gen9

    1484896133615587498: "dmkr48/gen10", #ella gen10
    1484896181342437376: "dmkr48/gen10", #lia gen10
    1484896189634711763: "dmkr48/gen10", #lyn gen10
    1484896215236743289: "dmkr48/gen10", #raisha gen10
    
    1484896090800001074: "dmkr48/gen11", #Alya gen11
    1484896098945339573: "dmkr48/gen11", #Anin gen11
    1484896102489784392: "dmkr48/gen11", #Cathy gen11
    1484896106210132099: "dmkr48/gen11", #Chelsea gen11
    1484896114762317994: "dmkr48/gen11", #Cynthia gen11
    1484896118197190776: "dmkr48/gen11", #Daisy gen11
    1484896121309630515: "dmkr48/gen11", #Danella gen11
    1484896129836384470: "dmkr48/gen11", #Elin gen11
    1484896153702109187: "dmkr48/gen11", #Gracie gen11
    1484896157850275981: "dmkr48/gen11", #Greesel gen11
    1484896198782615693: "dmkr48/gen11", #Michie gen11

    1484896220408184974: "dmkr48/gen12", #Aralie gen12
    1484908841031307285: "dmkr48/gen12", #Delynn gen12
    1484896230411866208: "dmkr48/gen12", #Erine gen12
    1484896234459369603: "dmkr48/gen12", #Fritzy gen12
    1484896268290621570: "dmkr48/gen12", #Kimmy gen12
    1484896226406301697: "dmkr48/gen12", #Lana gen12
    1484896246077591603: "dmkr48/gen12", #Levi gen12
    1484896237931991090: "dmkr48/gen12", #Lily gen12
    1484896253429940314: "dmkr48/gen12", #Nachia gen12
    1484896263928283146: "dmkr48/gen12", #Nala gen12
    1484896250015907860: "dmkr48/gen12", #Nayla gen12
    1484896256672399410: "dmkr48/gen12", #Oline gen12
    1484896260006608896: "dmkr48/gen12", #Ribka gen12
    1484896242109775902: "dmkr48/gen12", #Trisha gen12
}

def dispatch_files():
    # Look for all JSON files in the 'json' folder
    json_folder = Path("json")
    for json_file in json_folder.glob("*.json"):
        with open(json_file, "r") as f:
            data = json.load(f)
            
        # Get channel_id from the first message
        messages = data if isinstance(data, list) else data.get("messages", [])
        if not messages:
            continue
            
        channel_id = int(messages[0].get("channel_id", 0))
        target_repo = REPO_MAP.get(channel_id)

        if target_repo:
            print(f"Routing {json_file.name} to {target_repo}...")
            
            # This 'gh' command pushes the file directly to the other repo
            # without you having to manually clone it.
            subprocess.run([
                "gh", "repo", "deploy-key", "add", # or use PAT
                "gh", "api",
                f"/repos/{target_repo}/contents/json/{json_file.name}",
                "-X", "PUT",
                "-F", f"message=Dispatching JSON for {channel_id}",
                "-F", f"content=$(base64 -w 0 {json_file})",
                "-F", "branch=main"
            ])

if __name__ == "__main__":
    dispatch_files()