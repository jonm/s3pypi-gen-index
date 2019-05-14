# Copyright 2019 Jonathan T. Moore
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

VERSION = 0.1.1

all: s3pypi-gen-index-$(VERSION).zip

.dep: requirements.txt
	pip install -r requirements.txt -t .
	touch .dep

s3pypi-gen-index-$(VERSION).zip: .dep handler.py
	python -m compileall .
	rm -f s3pypi-gen-index-$(VERSION).zip
	zip -r s3pypi-gen-index-$(VERSION).zip . -x .git/\* -x \.* -x \*~ -x Makefile

clean:
	rm -f *.pyc s3pypi-gen-index-$(VERSION).zip *~

distclean: clean
	rm -f .dep

depend: .dep
