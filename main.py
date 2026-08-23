name: Build KharidYar APK

on:
  workflow_dispatch:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-22.04

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Java 17
        uses: actions/setup-java@v5
        with:
          distribution: temurin
          java-version: "17"

      - name: Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: System packages
        run: |
          sudo apt-get update
          sudo apt-get install -y \
            git zip unzip \
            openjdk-17-jdk \
            autoconf automake libtool \
            pkg-config zlib1g-dev \
            libncurses5-dev libncursesw5-dev \
            libtinfo5 cmake \
            libffi-dev libssl-dev \
            build-essential

      - name: Install Buildozer
        run: |
          python -m pip install --upgrade pip
          python -m pip install setuptools wheel
          python -m pip install "cython==0.29.34"
          python -m pip install buildozer

      - name: Force p4a master
        run: |
          git clone --depth 1 \
            --branch master \
            https://github.com/kivy/python-for-android.git \
            "$HOME/p4a"

          python -m pip install "$HOME/p4a"

      - name: Verify versions
        run: |
          python --version
          buildozer --version
          p4a --version

      - name: Clean
        run: |
          rm -rf .buildozer
          rm -rf bin

      - name: Build APK
        run: |
          yes | buildozer -v android debug

      - name: Verify APK
        run: |
          find bin -type f -name "*.apk" -print
          test -n "$(find bin -type f -name '*.apk' -print -quit)"

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: KharidYar-APK
          path: bin/*.apk
          if-no-files-found: error
