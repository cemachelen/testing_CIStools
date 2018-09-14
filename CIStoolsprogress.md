# CIS tools progress #

1. Mark has emailed Masaru's plugin emails

2. Installed CIS
  The environment is important
  ```bash
  module load anaconda3
  source ~/.local/bin/activate.sh
  conda create -c conda-forge -n cis_env cis   
  conda activate cis_env
  ```

3. Copied Plugins to `~/CIS/plugins`
  ```bash
   export CIS_PLUGIN_HOME=$HOME/cis/plugins
   ```
4. Copied over Masaru's data to CIS/CIStools_workspace/Masaru

5. Masaru's command:
  ```bash
    cis col -q od550aer:simulations/od550aer_IPSL_PDv2_CRESCENDOWP6_20100101_10h30m_loc.nc:product=IPSL_daily measurement/g4.subsetted.MOD08_D3_6_1_AOD_550_Dark_Target_Deep_Blue_Combined_Mean.20100101.180W_90S_180E_90N.nc:collocator=box[h_sep=156km],kernel=nn_t -o od550aer_IPSL_PDv2_CRESCENDOWP6_20100101_10h30m_loc_col_MOD08_D3.nc
    ```
6. Error reproduced:

  An error occurred retrieving data using the product IPSL_daily. Check that this is the correct product plugin for your chosen data. Exception was ValueError: operands could not be broadcast together with shapes (20592,) (144,) (20592,) .
  2018-09-13 14:09:36,200 - ERROR - An error occurred retrieving data using the product IPSL_daily. Check that this is the correct product plugin for your chosen data. Exception was ValueError: operands could not be broadcast together with shapes (20592,) (144,) (20592,).

7. Masaru's plugin is IPSL daily
   The error looks like he's missing a .T (transpose) somewhere

8. Understanding the command:
  * col = Perform collocation
  * -q = supress output
  * `cis col <datagroup> <samplegroup> -o <outputfile>`
  * `<datagroup> = <variable>...:<filename>[:product=<productname>]`
  * `<samplegroup> = <filename>[:<options>]`
  * collocator = search box with 156km separation
  * kernel: nn_t (or nn_time) - nearest neighbour in time algorithm
  * `-o <outputfile>`
9. 
