# CIS tools notes #

A repository of my progress in familiarising with CIStools. Focusing on notes and plugin writing

## Requirements ##
 
* Installed CIS
  The environment is important
  ```bash
  module load anaconda3
  source ~/.local/bin/activate.sh
  conda create -c conda-forge -n cis_env cis   
  conda activate cis_env
  ```

## Plugins ##
 
Plugins to `~/CIS/plugins`
  ```bash
   export CIS_PLUGIN_HOME=$HOME/cis/plugins
   ```

## Notes ##
command descriptions:
  * col = Perform collocation
  * -q = supress output
  * `cis col <datagroup> <samplegroup> -o <outputfile>`
  * `<datagroup> = <variable>...:<filename>[:product=<productname>]`
  * `<samplegroup> = <filename>[:<options>]`
  * collocator = search box with 156km separation
  * kernel: nn_t (or nn_time) - nearest neighbour in time algorithm
  * `-o <outputfile>`
