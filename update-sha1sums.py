#!/usr/bin/env python
#
# Copyright (C) 2016 The CyanogenMod Project
# Copyright (C) 2017-2018 The LineageOS Project
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from hashlib import sha1
import os
import sys

device = 'samurai'
vendor = 'realme'

lines = [line for line in open('proprietary-files.txt', 'r')]
vendorPath = f'../../../vendor/{vendor}/{device}/proprietary'
needSHA1 = False

def cleanup():
    for index, line in enumerate(lines):
        line = line.rstrip('\n')
        if not line or line.startswith('#'):
            continue
        if '|' in line:
            line = line.split('|')[0]
            lines[index] = f'{line}\n'

def update():
    global needSHA1
    for index, line in enumerate(lines):
        line = line.rstrip('\n')
        if not line:
            continue
        if line.startswith('#'):
            needSHA1 = ' - from' in line
            continue
        if needSHA1:
            line = line.split('|')[0]
            filePath = line.split(':')[1] if ':' in line else line
            filePath = filePath.split(';')[0]  # Remove any extra parameters like SYMLINK

            if filePath.startswith('-'):
                filePath = filePath[1:]

            fullPath = os.path.join(vendorPath, filePath)

            if not os.path.exists(fullPath):
                print(f"File not found: {fullPath}")
                continue

            try:
                with open(fullPath, 'rb') as f:
                    file = f.read()
                hash = sha1(file).hexdigest()
                lines[index] = f'{line}|{hash}\n'
            except Exception as e:
                print(f"Error reading file {fullPath}: {e}")

if len(sys.argv) == 2 and sys.argv[1] == '-c':
    cleanup()
else:
    update()

with open('proprietary-files.txt', 'w') as file:
    file.writelines(lines)
