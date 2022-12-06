# List of snippets of interesting code

### 1.- Error
```
	(tf_gpu_mygames) PS C:\Users\metol\Downloads> git clone https://github.com/openai/baselines
	Cloning into 'baselines'...
	remote: Enumerating objects: 3627, done.
	remote: Total 3627 (delta 0), reused 0 (delta 0), pack-reused 3627
	Receiving objects: 100% (3627/3627), 6.46 MiB | 9.65 MiB/s, done.
	Resolving deltas: 100% (2429/2429), done.
	(tf_gpu_mygames) PS C:\Users\metol\Downloads> cd .\baselines\
	(tf_gpu_mygames) PS C:\Users\metol\Downloads\baselines> pip install .
	Processing c:\users\metol\downloads\baselines
	  Preparing metadata (setup.py) ... done
	Collecting gym<0.16.0,>=0.15.4
	  Downloading gym-0.15.7.tar.gz (1.6 MB)
	     ---------------------------------------- 1.6/1.6 MB 11.0 MB/s eta 0:00:00
	  Preparing metadata (setup.py) ... done
	Requirement already satisfied: scipy in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from baselines==0.1.6) (1.6.3)
	Collecting tqdm
	  Downloading tqdm-4.64.1-py2.py3-none-any.whl (78 kB)
	     ---------------------------------------- 78.5/78.5 KB ? eta 0:00:00
	Requirement already satisfied: joblib in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from baselines==0.1.6) (0.17.0)
	Requirement already satisfied: cloudpickle in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from baselines==0.1.6) (2.2.0)
	Collecting click
	  Using cached click-8.1.3-py3-none-any.whl (96 kB)
	Collecting opencv-python
	  Downloading opencv_python-4.6.0.66-cp36-abi3-win_amd64.whl (35.6 MB)
	     ---------------------------------------- 35.6/35.6 MB 11.7 MB/s eta 0:00:00
	Requirement already satisfied: numpy>=1.10.4 in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from gym<0.16.0,>=0.15.4->baselines==0.1.6) (1.22.2)
	Requirement already satisfied: six in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from gym<0.16.0,>=0.15.4->baselines==0.1.6) (1.15.0)
	Collecting pyglet<=1.5.0,>=1.4.0
	  Downloading pyglet-1.5.0-py2.py3-none-any.whl (1.0 MB)
	     ---------------------------------------- 1.0/1.0 MB 13.0 MB/s eta 0:00:00
	Collecting cloudpickle
	  Downloading cloudpickle-1.2.2-py2.py3-none-any.whl (25 kB)
	Requirement already satisfied: colorama in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from click->baselines==0.1.6) (0.4.4)
	Requirement already satisfied: future in c:\users\metol\.conda\envs\tf_gpu_mygames\lib\site-packages (from pyglet<=1.5.0,>=1.4.0->gym<0.16.0,>=0.15.4->baselines==0.1.6) (0.18.2)
	Building wheels for collected packages: baselines, gym
	  Building wheel for baselines (setup.py) ... done
	  Created wheel for baselines: filename=baselines-0.1.6-py3-none-any.whl size=222451 sha256=dcf5fc6144e932bdf4bbc1230a563dbdfbf543e47eb50f00fed75e78ed85a8c2
	  Stored in directory: C:\Users\metol\AppData\Local\Temp\pip-ephem-wheel-cache-r2unacid\wheels\95\45\e7\dcd08d5c5c44be55d57f1d5d71c63bbeab6318fae0d974e8ed
	  Building wheel for gym (setup.py) ... done
	  Created wheel for gym: filename=gym-0.15.7-py3-none-any.whl size=1648842 sha256=68fdfca401253d345b8a48070ce276d41ef79c95ae6df71172b282fffeaf5761
	  Stored in directory: c:\users\metol\appdata\local\pip\cache\wheels\42\c9\4b\5043e144d4319a7ebe7d59be1ad561ed129edecfa73300f096
	Successfully built baselines gym
	Installing collected packages: cloudpickle, tqdm, pyglet, opencv-python, click, gym, baselines
	  Attempting uninstall: cloudpickle
	    Found existing installation: cloudpickle 2.2.0
	    Uninstalling cloudpickle-2.2.0:
	      Successfully uninstalled cloudpickle-2.2.0
	  Attempting uninstall: pyglet
	    Found existing installation: pyglet 1.5.16
	    Uninstalling pyglet-1.5.16:
	      Successfully uninstalled pyglet-1.5.16
	  Attempting uninstall: gym
	    Found existing installation: gym 0.21.0
	    Uninstalling gym-0.21.0:
	ERROR: Could not install packages due to an OSError: [WinError 32] The process cannot access the file because it is being used by another process: 'c:\\users\\metol\\.conda\\envs\\tf_gpu_mygames\\lib\\site-packages\\gym\\'
	Consider using the `--user` option or check the permissions.
 ```

