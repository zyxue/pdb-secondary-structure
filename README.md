This repo records details of how the protein secondary structure data is curated.


#### Download secondary structure data

```
DATE_STAMP=$(date  +'%Y-%m-%d')
wget https://cdn.rcsb.org/etl/kabschSander/ss.txt.gz -O ${DATE_STAMP}-ss.txt.gz
```

#### Transform to csv format
```
python transform_ss_txt_to_csv.py -i ${DATE_STAMP}-ss.txt.gz
```

#### Download PISCES data, removed peptides with high similarity

https://academic.oup.com/bioinformatics/article/19/12/1589/258419

```
wget http://dunbrack.fccc.edu/Guoli/culledpdb_hh/cullpdb_pc25_res2.0_R0.25_d180531_chains9099.gz
```

If the above URL doesn't work, update it according to http://dunbrack.fccc.edu/Guoli/culledpdb_hh/.

Interpretation of the filename based on http://dunbrack.fccc.edu/Guoli/pisces_download.php: 

* `pc25`:  the percentage identity cutoff is 25%
* `res2.0`: he resolution cutoff is 2.0 angstroms
* `R0.25`: the R-factor cutoff is 0.25
* `d180531`: datestamp
* `chains9099`: the number of sequences in the file

In addition:

* `inclNOTXRAY`: include sequences from non-xray-derived structures (mostly NMR but also including electron diffraction, FTIR, fiber diffraction, etc.). 
* `inclCA`: include sequences of structures that contain only backbone CA coordinates.

#### Related Kaggle page:

https://www.kaggle.com/alfrandom/protein-secondary-structure
