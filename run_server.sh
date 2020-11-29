#!/bin/sh

bundle update
bundle exec jekyll serve
echo "http://localhost:4000 is ready and waiting."
