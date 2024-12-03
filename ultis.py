import dataclasses
from typing import Dict, List, Optional
from browserforge.fingerprints import FingerprintGenerator, Fingerprint, ScreenFingerprint, NavigatorFingerprint, VideoCard
import json


def create_fingerprint(profile, os):
    fingerprints = FingerprintGenerator()
    fingerprint_data = fingerprints.generate(
        browser='chrome', os=os)
    aaa = json.dumps(dataclasses.asdict(fingerprint_data))
    with open(f'fingerprint_folder/{profile}.json', 'w') as f:
        f.write(aaa)
    return fingerprint_data


def load_fingerprint(profile):
    path = f'fingerprint_folder/{profile}.json'
    with open(path, 'r') as f:
        data = json.load(f)
        screen = ScreenFingerprint(**data['screen'])
        navigator = NavigatorFingerprint(**data['navigator'])
        headers = data['headers']
        videoCodecs = data['videoCodecs']
        audioCodecs = data['audioCodecs']
        pluginsData = data['pluginsData']
        battery = data['battery']
        videoCard = VideoCard(**data['videoCard'])
        multimediaDevices = data['multimediaDevices']
        fonts = data['fonts']
        mockWebRTC = data['mockWebRTC']
        slim = data['slim']
        return Fingerprint(
            screen=screen,
            navigator=navigator,
            headers=headers,
            videoCodecs=videoCodecs,
            audioCodecs=audioCodecs,
            pluginsData=pluginsData,
            battery=battery,
            videoCard=videoCard,
            multimediaDevices=multimediaDevices,
            fonts=fonts,
            mockWebRTC=mockWebRTC,
            slim=slim
        )
