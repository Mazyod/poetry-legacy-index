# Poetry Legacy Index Fix

This project is a poetry plugin that has one simple purpose:

**Patch poetry (Legacy) Repository to download wheels associated with the given platform.**

## Why?

Long story short, TensorFlow 2.11.x includes different metadata per platform wheel, and poetry simply downloads the first wheel found in a legacy index (e.g. devpi, pypiserver), which causes it to incorrectly resolve the dependencies.

Another nice side effect is that (based on a discussion on the poetry repo) poetry doesn't cache the downloaded wheels at the "solving" phase, which means that if the first wheel downloaded is not the one that will be installed, it will be downloaded again and again each time (~500 MB for TensorFlow). By downloading the wheel for the given platform, it will *at least* check the cache before attempting to download the wheel, and the wheel should be available if it was already downloaded for installation.
