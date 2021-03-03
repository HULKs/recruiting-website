# Motion Task

<x-prologue image="recruiting-website-motion" command="bash -c 'cp /usr/src/app/{generate_animation.py,*.png} /data/ && echo Initialized files.'" />

<x-text-editor file="/data/generate_animation.py" mode="python" />

<x-button image="recruiting-website-motion" command="python generate_animation.py" label="Run program" working-directory="/data" />

<x-image-viewer file="/data/animation.gif" mime="image/gif" />
