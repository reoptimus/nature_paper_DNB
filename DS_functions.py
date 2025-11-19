####### FUNCTION USED in the code  ########
import pandas as pd
import numpy as np
import os
import importlib
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

# load functions used to clean, merun and write DS and vulnerabilities values per country/sector/ecosystem services
def ND_GAIN_Tab_generator(Nature_indice_path, path_ISO):
    # Example: path_ISO = "I:\\...\\Misc_tables\\"
    # Example: Nature_indice_path = "I:\\...\\ND-GAIN index\\resources\\vulnerability\\"
    ND_GAIN_tab = pd.read_csv(Nature_indice_path+'ecosystems.csv')
    ND_GAIN_tab.fillna(0, inplace=True) # clean nan
    ND_GAIN_tab = ND_GAIN_tab.iloc[:,[0,1,-1]]# keep the last column 2021
    ND_GAIN_tab.rename(columns= {'2021':'ecosystems'},inplace=True)# rename columns

    a=pd.read_csv(Nature_indice_path+'water.csv')
    a.fillna(0, inplace=True)
    a = a.iloc[:,[0,1,-1]]
    a.rename(columns= {'2021':'water'},inplace=True)
    ND_GAIN_tab = pd.merge(ND_GAIN_tab,a,on=['ISO3', 'Name'], how='left')

    a=pd.read_csv(Nature_indice_path+'habitat.csv')
    a.fillna(0, inplace=True)
    a = a.iloc[:,[0,1,-1]]
    a.rename(columns= {'2021':'habitat'},inplace=True)
    a.columns
    ND_GAIN_tab = pd.merge(ND_GAIN_tab,a,on=['ISO3', 'Name'], how='left')

    a=pd.read_csv(Nature_indice_path+'food.csv')
    a.fillna(0, inplace=True)
    a = a.iloc[:,[0,1,-1]]
    a.rename(columns= {'2021':'food'},inplace=True)
    a.columns
    ND_GAIN_tab = pd.merge(ND_GAIN_tab,a,on=['ISO3', 'Name'], how='left')

    # import code country equivalency table
    tab_country_code = pd.read_csv(path_ISO+'Code_country_ISO2_ISO3.csv')
    # replace country code ISO3 by ISO2
    ND_GAIN_tab = pd.merge(ND_GAIN_tab,tab_country_code,on=['ISO3', 'Name'], how='left')
    ND_GAIN_tab = ND_GAIN_tab.iloc[:,2:]
    ND_GAIN_tab =ND_GAIN_tab.rename(columns = {'ISO2':'region'})
    return ND_GAIN_tab

def read_clean_ENCORE(path_to_file,rating_mapping):
    encore_dependencies_materialities = pd.read_csv(path_to_file, header=0)
    list_ES = encore_dependencies_materialities.columns[6:]
    #########################################
    # cleaning procedure of raw ENCORE data
    # Select columns and rename them
    encore_dependencies_materialities = (
        encore_dependencies_materialities
        .drop(columns=['ISIC Section', 'ISIC Division', 'ISIC Group','ISIC Class', 'ISIC level used for analysis '])
        .melt(id_vars='ISIC Unique code', var_name='eco_serv', value_name='rating')
        .rename(columns={'ISIC Unique code': 'process'}) )
    ### ATTENTION 1 ###
    # 'D_35_351' : multiple class for one ISIC unique code Energy
    ########## ATTENTION 2: where the numerical grid is!!! #######################
    
    #########    Mapping qualitative to quantitative ENCORE value    ###########
    encore_dependencies_materialities['rating_int'] = (
        encore_dependencies_materialities['rating'].map(rating_mapping).fillna(0) )

    encore_dependencies_final = (
        encore_dependencies_materialities[['process', 'eco_serv', 'rating_int']]
        .drop_duplicates()
        .sort_values(['process', 'rating_int'], ascending=[True, False])
        .reset_index(drop=True) )
    return encore_dependencies_final

def isic2nace_clean(isic2nace_raw_path,encore_dependencies_final): # isic2nace_raw_path=isic2nace_raw_path = 'I:\\FS\\FS\\Statsp\\000-Beleidsmedewerkers\\Sebastien Gallet\\Biodiv\\OS-2025\\downloaded_data\\ENCORE\\ENCORE files October 2024_072025\\' + '14. EXIOBASE NACE ISIC crosswalk.csv'
    isic2nace_raw = pd.read_csv( isic2nace_raw_path)
    isic2nace = pd.concat([
        encore_dependencies_final.merge(isic2nace_raw, how='left', left_on='process', right_on='ISIC Unique Group code'),
        encore_dependencies_final.merge(isic2nace_raw, how='left', left_on='process', right_on='ISIC Unique Class code')
    ], ignore_index=True)
    isic2nace = (isic2nace
        .sort_values('ISIC Unique Class code', na_position='last')
        .drop_duplicates(['process', 'eco_serv'])
        .drop(columns=['process','NACE class','NACE Code and Level','ISIC Class', 'ISIC Group', 'ISIC Division', 'ISIC Section'])
        .reset_index(drop=True)
    )
    return isic2nace

def building_L_matrix(EXIOBASE_A_matrix_path):
    A = pd.read_csv(EXIOBASE_A_matrix_path, header=None , low_memory=False )
    # List_cntry_sect = A.loc[2:, [0, 1]].rename(columns={0: 'region', 1: 'EXIOBASE'}).reset_index(drop=True)
    A_clean = A.iloc[2:, 2:].astype(float)
    # Compute Leontief inverse
    I = np.eye(len(A_clean))
    L = np.linalg.inv(I - A_clean)
    # Normalize (L - I) by column sums
    L_I_bar = L - I
    L_I_bar = L_I_bar / L_I_bar.sum(axis=0)
    L_I_bar = pd.DataFrame(L_I_bar).fillna(0)
    # put 1 in diag if col sum = 0
    L_I_bar_np = L_I_bar.to_numpy()
    mask = (L_I_bar_np.sum(axis=0) == 0)
    np.fill_diagonal(L_I_bar_np, np.where(mask, 1, np.diag(L_I_bar_np)))
    L_I_bar = pd.DataFrame(L_I_bar_np, index=L_I_bar.index, columns=L_I_bar.columns) # convert it back to a DataFrame
    # L_I_bar.sum(axis=0) ; L_I_bar.head() ; np.shape(L_I_bar) ; type(L_I_bar) #  # control, must be equal of a vector of 1 or 0s
    return L_I_bar,A

def subcontract_ratio(Z_path,X_path,List_cntry_sect):
    # Replace with actual data loading
    Z = pd.read_csv(Z_path, header=None , low_memory=False) # Interindustry transaction matrix
    Z_clean = Z.iloc[2:, 2:].astype(float).values
    X = pd.read_csv(X_path, header=0) # Total output vector
    # Calculate SR for each industry
    np.fill_diagonal(Z_clean, 0) # modifies Z_clean directly to not account for intra country/sectorial flows as subcontracting
    intermediate_inputs = np.sum(Z_clean, axis=0)  # Sum over rows for each column
    SR = np.divide(intermediate_inputs, X["indout"].values, out=np.zeros_like(intermediate_inputs), where=X["indout"].values!=0)
    SR_mat = List_cntry_sect
    SR_mat['SR'] = np.array(SR).reshape(-1, 1)  # horizontally stack of SR as a column
    return SR_mat,X

def PCA_analysis(isic2nace):
    # Create PCA input tables
    encore_dependencies_PCA = isic2nace[['NACElevel','eco_serv','rating_int']].drop_duplicates()
    # encore_dependencies_PCA['eco_serv'].unique()
    encore_dependencies_PCA_final = encore_dependencies_PCA.pivot_table(index='eco_serv', columns='NACElevel', values='rating_int', aggfunc='max')
    # encore_dependencies_PCA_final = encore_dependencies_PCA.pivot_table(index='eco_serv', columns='NACElevel', values='rating_int', aggfunc='mean')
    #### PCA Analysis ##################################################################
    # definie Var and Fill missing values (if any)
    X = encore_dependencies_PCA_final.fillna(0)
    # Standardize the data
    X_scaled = StandardScaler().fit_transform(X)
    # Apply PCA
    pca = PCA(n_components=2)  # You can adjust components
    X_pca = pca.fit_transform(X_scaled)
    # Create a DataFrame of Results
    pca_df = pd.DataFrame(X_pca, columns=['PC1', 'PC2'], index=X.index)
    ### Clustering #####################
    from sklearn.cluster import KMeans
    k = 3  # You can change this based on your elbow method or domain knowledge
    kmeans = KMeans(n_clusters=k, random_state=42)
    clusters = kmeans.fit_predict(X_pca)
    pca_df['cluster'] = clusters

    # plt.figure(figsize=(10, 6))
    # for i in range(k):
    #     plt.scatter(X_pca[clusters == i, 0], X_pca[clusters == i, 1], label=f'Cluster {i+1}')

    # # Annotate points with eco_serv labels
    # for i, label in enumerate(X.index):
    #     plt.text(X_pca[i, 0], X_pca[i, 1], label, fontsize=8, alpha=0.6)

    # plt.xlabel('Principal Component 1')
    # plt.ylabel('Principal Component 2')
    # plt.title('PCA with K-means Clustering of Ecosystem Services')
    # plt.legend()
    # plt.grid(True)
    # plt.tight_layout()
    # plt.show()
    return pca_df

def merge_public_admin_vulnerability(DS_file):
    # Define constants
    EXIOBASE_gov_name = 'Public administration and defence; compulsory social security (75)'
    cols_to_update = ['DS_total_max', 'DS_total_SR', 'Vuln_total_max', 'Vuln_total_SR'    ]

    # Get unique values
    list_ES = DS_file['eco_serv'].drop_duplicates()
    list_country = DS_file['region'].drop_duplicates()

    # Initialize empty DataFrame
    new_vul_gov_table = pd.DataFrame(columns=['region', 'eco_serv', 'EXIOBASE'] + cols_to_update)

    # Loop through combinations of countries and ecosystem services
    for region in list_country:
        for eco_serv in list_ES:
            sub_DS = DS_file[(DS_file['region'] == region) & (DS_file['eco_serv'] == eco_serv)]
            if sub_DS.empty or sub_DS['indout'].sum() == 0:
                continue  # Avoid division by zero or empty data

            new_line = {
                'region': region,
                'eco_serv': eco_serv,
                'EXIOBASE': EXIOBASE_gov_name
            }

            for col in cols_to_update:
                weighted_avg = (sub_DS[col] * sub_DS['indout']).sum() / sub_DS['indout'].sum()
                new_line[col] = weighted_avg
            # Only append if new_line has valid data
            new_vul_gov_table = pd.concat([new_vul_gov_table, pd.DataFrame([new_line])], ignore_index=True)

    # Merge new vulnerability data into DS_file
    merged = DS_file.merge(
        new_vul_gov_table,
        on=['region', 'eco_serv', 'EXIOBASE'],
        how='left',
        suffixes=('', '_new')
    )

    # Update columns with new values where available
    for col in cols_to_update:
        merged[col] = merged[col].where(merged[col + '_new'].isna(), merged[col + '_new'])

    # Drop temporary columns
    merged.drop(columns=[col + '_new' for col in cols_to_update], inplace=True)

    return merged

def merge_fin_vulnerability(DS_file, List_cntry_sect, ratio_Gov_on_NFCpGov=0.5):
    ratio_NFC_on_NFCpGov = 1 - ratio_Gov_on_NFCpGov

    List_cntry = List_cntry_sect['region'].drop_duplicates()
    list_financial_sector = DS_file[DS_file['NACE Code'].isin([64, 65, 66])][['EXIOBASE', 'NACE Code']].drop_duplicates()
    list_gov_sector = DS_file[DS_file['NACE Code'].isin([84])][['EXIOBASE', 'NACE Code']].drop_duplicates()

    merged = DS_file.copy()
    cols_to_update = ['DS_total_max', 'DS_total_SR', 'Vuln_total_max', 'Vuln_total_SR']
    new_vul_fin_table = pd.DataFrame(columns=['region', 'eco_serv', 'EXIOBASE'] + cols_to_update)

#########################
# should be done on Assets values in place of indout (production per sector from EXIOBASE)
    for country in List_cntry:
        country_data = DS_file[DS_file['region'] == country].copy()
        fin_indout_sum = country_data[country_data['EXIOBASE'].isin(list_financial_sector['EXIOBASE'])]['indout'].sum()
        gov_indout_sum = country_data[country_data['EXIOBASE'].isin(list_gov_sector['EXIOBASE'])]['indout'].sum()
        total_indout_excl_fin_gov = country_data['indout'].sum() - fin_indout_sum - gov_indout_sum

        country_data['Asset_ratio'] = country_data['indout'] / total_indout_excl_fin_gov
        country_data['Asset_ratio'] *= ratio_NFC_on_NFCpGov

        # Zero out financial sector
        mask_fin = country_data['EXIOBASE'].isin(list_financial_sector['EXIOBASE'])
        country_data.loc[mask_fin, 'Asset_ratio'] = 0

        # Adjust government sector
        mask_gov = country_data['EXIOBASE'].isin(list_gov_sector['EXIOBASE'])
        country_data.loc[mask_gov, 'Asset_ratio'] = (
            total_indout_excl_fin_gov / gov_indout_sum / ratio_NFC_on_NFCpGov * ratio_Gov_on_NFCpGov
        )

        sub_merged = pd.merge(
            merged[merged['region'] == country][[
                'region', 'EXIOBASE', 'eco_serv'] + cols_to_update].drop_duplicates(),
            country_data[['region', 'EXIOBASE', 'Asset_ratio']].drop_duplicates(),
            on=['region', 'EXIOBASE'],
            how='left'
        )

        for ES in sub_merged['eco_serv'].drop_duplicates():
            tab = sub_merged[sub_merged['eco_serv'] == ES]
            for exiobase in list_financial_sector['EXIOBASE']:
                new_line = {
                    'region': country,
                    'eco_serv': ES,
                    'EXIOBASE': exiobase
                }
                for col in cols_to_update:
                    weighted_avg = (tab[col] * tab['Asset_ratio']).sum() / tab['Asset_ratio'].sum()
                    new_line[col] = weighted_avg
                new_vul_fin_table = pd.concat([new_vul_fin_table, pd.DataFrame([new_line])], ignore_index=True)

    # Merge new vulnerability data into DS_file
    merged = merged.merge(
        new_vul_fin_table,
        on=['region', 'eco_serv', 'EXIOBASE'],
        how='left',
        suffixes=('', '_new')
    )

    # Update columns with new values where available
    for col in cols_to_update:
        merged[col] = merged[col].where(merged[col + '_new'].isna(), merged[col + '_new'])

    # Drop temporary columns
    merged.drop(columns=[col + '_new' for col in cols_to_update], inplace=True)

    return merged

def alpha_calculation(shock_area , path_DS_store_ , ds_table , files_name , tab_area_country_code ): # shock_area=config.data_shock ; path_DS_store_= config.path_DS_store ; ds_table = DS_file ;files_name= Alpha_name ; tab_area_country_code= config.tab_area_country_code
    # preparation
    # ds_table = pd.read_csv(path_DS_store_ + files_name)
    ds_table = ds_table.merge(tab_area_country_code, on = 'region', how = 'left')
    ds_table['Area'] = ds_table['area'].fillna('not defined')
    # Define indicators
    all_indicators = ['DS_total_SR', 'DS_total_max', 'Vuln_total_SR', 'Vuln_total_max']
    # Initialize results with Area and eco_serv
    results = ds_table[['Area', 'eco_serv']].drop_duplicates().copy()
    # Compute alpha for each indicator
    for col in all_indicators: # col='Vuln_total_SR'
        temp = ds_table[['Area', 'eco_serv', 'indout', col]].copy()
        temp['weighted'] = temp['indout'] * temp[col]
        grouped = temp.groupby(['Area', 'eco_serv'], as_index=False).agg(
            indout_sum=('indout', 'sum'),
            weighted_sum=('weighted', 'sum')
        )
        grouped[f'{col}_alpha'] = grouped['weighted_sum'] / grouped['indout_sum']
        results = results.merge(grouped[['Area', 'eco_serv', f'{col}_alpha']], on=['Area', 'eco_serv'], how='left')

    # Merge with shock_area and compute final alpha values
    results = results.merge(shock_area, on='Area')
    for col in all_indicators:
        alpha_col = f'{col}_alpha'
        results[alpha_col] = results['Production shock'] / results[alpha_col]
    # store the table as xlsx   
    if files_name.endswith(".csv"):
        files_name = files_name[:-4]
    results.to_excel( path_DS_store_ + 'DS_Vuln_files_stored\\' + files_name + '.xlsx', index=False )
    return

def DS_file_calculation(path_DS_store_ , confg_file_name): #  confg_file_name = 'config_0_World_shock_10perc_02_GOVonNFC'
    os.chdir( path_DS_store_ + 'config_store\\' )
    config = importlib.import_module(confg_file_name)
    # importlib.reload(config)
    ###########################
    # Read and clean the ENCORE CSV file : '06. Dependency mat ratings.csv'
    encore_dependencies_final = read_clean_ENCORE(config.path_to_file,config.rating_mapping) # type: ignore
    ################################################
    # ISIC to NACE code: ENCORE correspondance table
    # Read the ENCORE ISIC NACE correspondance table CSV file into a DataFrame
    isic2nace = isic2nace_clean(config.isic2nace_raw_path,encore_dependencies_final)
    #######################################
    # Buiding up of L matrix 
    # import of the MR-IO "A" matrix
    L_I_bar,A = building_L_matrix(config.EXIOBASE_A_matrix_path)
    #######################################
    # DS direct and indirect (without nature degradation indice)
    #######################################
    # calculation of Indirect DS with DS X (L-I) -> see ECB note
    # shape DS direct similar to L_I_bar
    List_cntry_sect = A.loc[2:, [0, 1]].rename(columns={0: 'region', 1: 'EXIOBASE'}).reset_index(drop=True)
    DS_direct = (
        pd.merge(List_cntry_sect, isic2nace, on='EXIOBASE', how='left') [['region', 'EXIOBASE', 'eco_serv', 'rating_int']]
        .fillna({'rating_int': 0})
        .drop_duplicates()
        .reset_index(drop=True) )
    DS_file = pd.DataFrame()
    for ES in DS_direct['eco_serv'].drop_duplicates(): # ES = 'Biomass provisioning'
        # Filter and select max rating per sector
        filtered = DS_direct.query("eco_serv == @ES").drop_duplicates()
        idx = filtered.groupby(['region', 'EXIOBASE'])['rating_int'].idxmax() # take the max in case several lines for same region/sector (due to process-sector correspondance table)
        DS_direct_per_ES = List_cntry_sect.merge(filtered.loc[idx], on=['region', 'EXIOBASE'], how='left') \
            .fillna({'eco_serv': ES, 'rating_int': 0}) \
            .rename(columns={'rating_int': 'DS_direct'})  
        # Compute indirect dependencies
        DS_indirect = DS_direct_per_ES['DS_direct'].T @  L_I_bar 
        DS_per_ES = DS_direct_per_ES.assign(DS_indirect=DS_indirect)
        DS_file = pd.concat([DS_file, DS_per_ES], ignore_index=True)
    DS_file = DS_file.dropna(subset=['eco_serv'])
    ######################################
    # calculation of subcontracted ratio per country/sector
    ######################################
    SR_mat,X = subcontract_ratio(config.Z_path,config.X_path,List_cntry_sect)
    DS_file = pd.merge(DS_file, SR_mat, on=["region", "EXIOBASE"], how="inner")
    #######################################
    # Vuln direct and indirect
    # New methodology including nature degradation index
    #######################################
    # step 1 : vuln direct is DS direct multiplied to nature degradation index par country
    # creation of the list of degradation index per country and per ES type
    ND_GAIN = ND_GAIN_Tab_generator(config.Nature_indice_path, config.path_ISO)
    # creation of the list of nature degradation indice per ES
    # comes from the PCA analysis
    pca_df = PCA_analysis(isic2nace)
    Corresp_list_ES_to_natureIndex = pca_df.reset_index()[['eco_serv', 'cluster']]# run the file DS_PCA_analysis.py to get this variable
    # correspondance with nature indice
    Nature_indic_corresp = pd.DataFrame( ['ecosystems', 'water', 'habitat'],index=[0, 1, 2],columns=['nature_indice_type'] ).reset_index()
    Nature_ES_relation = Corresp_list_ES_to_natureIndex.reset_index()[['eco_serv', 'cluster']].merge(Nature_indic_corresp, left_on='cluster', right_on='index').drop(['cluster','index'],axis=1)
    # Step 1.1: Merge DS_file with Nature_ES_relation to get the service type
    DS_enriched = DS_file.merge(Nature_ES_relation, on='eco_serv', how='left')
    # Step 1.2: Melt ND_gain so each service type becomes a row
    ND_melted = ND_GAIN.melt(id_vars='region', var_name='nature_indice_type', value_name='nature_indice')
    # Step 1.3: Merge DS_enriched with ND_melted on both country and service
    DS_final = DS_enriched.merge(ND_melted, on=['region', 'nature_indice_type'], how='left')
    DS_final = DS_final.fillna(0) # several small countries are missing in ND-GAIN, we impose Vuln to 0 in this case
    # step 2 : recalculation of vuln indirect based on vuln direct
    DS_final['Vuln_direct'] = DS_final['DS_direct'] * DS_final['nature_indice']
    DS_file = pd.DataFrame()
    for ES in DS_final['eco_serv'].drop_duplicates(): # ES = 'Biomass provisioning'
        # Filter and select max rating per sector
        filtered = DS_final.query("eco_serv == @ES").drop_duplicates().drop(columns=['SR'])
        idx = filtered.groupby(['region', 'EXIOBASE'])['Vuln_direct'].idxmax()
        Vuln_direct_per_ES = List_cntry_sect.merge(filtered.loc[idx], on=['region', 'EXIOBASE'], how='left') \
            .fillna({'eco_serv': ES, 'rating_int': 0}) \
            .rename(columns={'rating_int': 'DS_direct'})  
        # Compute indirect dependencies
        Vuln_indirect = Vuln_direct_per_ES['Vuln_direct'].T @  L_I_bar 
        Vuln_per_ES = Vuln_direct_per_ES.assign(Vuln_indirect=Vuln_indirect)
        DS_file = pd.concat([DS_file, Vuln_per_ES], ignore_index=True)
    DS_file = DS_file.dropna(subset=['eco_serv'])
    #####################################
    # calculation of DS and Vuln total
    #####################################
    # option 1: DS total is the weighted sum of DS direct and indirect weighted by Subcontract ratio (SR)
    DS_file["DS_total_SR"]=DS_file["DS_indirect"]*DS_file["SR"]+DS_file["DS_direct"]*(1-DS_file["SR"])
    # option 2: DS total is the Max() of DS direct and indirect
    DS_file["DS_total_max"]=np.maximum(DS_file["DS_indirect"],DS_file["DS_direct"])
    # option 1: Vuln total is the weighted sum of Vuln direct and indirect weighted by Subcontract ratio (SR)
    DS_file["Vuln_total_SR"]=DS_file["Vuln_indirect"]*DS_file["SR"]+DS_file["Vuln_direct"]*(1-DS_file["SR"])
    # option 2: Vuln total is the Max() of Vuln direct and indirect
    DS_file["Vuln_total_max"]=np.maximum(DS_file["Vuln_indirect"],DS_file["Vuln_direct"])
    #####################################
    # add adj_ind per NACE sector
    # add X the production per country/EXIOBASE sector
    #####################################
    X.rename(columns={'sector': 'EXIOBASE'}, inplace=True)
    DS_file = pd.merge(DS_file, X, on=['region', 'EXIOBASE'], how='left')
    # add columns NACE Code (integer only so lvl2)
    df = pd.read_csv(config.isic2nace_raw_path)
    df=df[['NACE Code','EXIOBASE']]
    df['NACE Code']=df['NACE Code'].astype(str).str.split(".").str[0].astype(int)
    # verification of duplicates: multi NACE code for one EXIOBASE sector
    # nace_counts = df.groupby('EXIOBASE')['NACE Code'].nunique()
    # duplicates = nace_counts[nace_counts>1] # show EXIOBASE entries with multiple NACE Code
    # keep the lowest NACE Code of duplicated and remove others
    df_cleaned = df.sort_values(by="NACE Code").drop_duplicates(subset='EXIOBASE', keep='first')
    DS_file = DS_file.merge(df_cleaned[['EXIOBASE','NACE Code']], on='EXIOBASE',how='left').copy()
    # cross with adjusted indicator per NACE (xlsx file)
    Adj_ind_by_industry = pd.read_excel(config.path_ISO+ config.adj_ind_file)
    Adj_ind_by_industry.rename(columns={'NACE code': 'NACE Code'}, inplace=True)
    # Keep row with max Adj_ind for each unique NACE code
    Adj_ind_by_industry_cleaned = Adj_ind_by_industry.loc[Adj_ind_by_industry.groupby('NACE Code')['Adj_ind'].idxmax()]
    # merge
    DS_file = DS_file.merge(Adj_ind_by_industry_cleaned[['NACE Code', 'Adj_ind']], on='NACE Code',how='left').copy()
    #####################################
    # Vuln_total and DS_total correction : not done here anymore
    #####################################
    # DS_file['DS_total_max_adj']=DS_file['DS_total_max']*DS_file['Adj_ind']
    # DS_file['DS_total_SR_adj']=DS_file['DS_total_SR']*DS_file['Adj_ind']
    # DS_file['Vuln_total_max_adj']=DS_file['Vuln_total_max']*DS_file['Adj_ind']
    # DS_file['Vuln_total_SR_adj']=DS_file['Vuln_total_SR']*DS_file['Adj_ind']
    #####################################
    # re-calculation of Vuln total for governments and finance
    #####################################
    # for governments
    
    # test and comparison
    # sub_DS_file_public_admin_modif = DS_file_modif_gov[DS_file_modif_gov['EXIOBASE']=='Public administration and defence; compulsory social security (75)'][sub_DS_file_public_admin.columns].copy()
    # df = sub_DS_file_public_admin_modif.merge(sub_DS_file_public_admin,on=['region','eco_serv'], how='left')
    # df['eco_serv'].drop_duplicates()
    # filtered_df = df[(df['region'].isin(['US', 'NL', 'FR', 'DE', 'IT', 'ES', 'UK'])) & (df['eco_serv'] == 'Water flow regulation')]
    # (filtered_df.iloc[:,2:6].values-filtered_df.iloc[:,6:11].values)/filtered_df.iloc[:,6:11].values
    # conclusion: new Vuln are 20 to 50% more important for public sector than when ENCORE value for gov is used
    # option to activate or not
    if config.activation_gov_vuln==1:
        merge = merge_public_admin_vulnerability(DS_file)
        DS_file = merge
    #####################################
    # for finance
    # first approx at world level to try but must be modified later!
    
    # test and comparison
    # cols_to_update = ['DS_total_max_adj', 'DS_total_SR_adj', 'Vuln_total_max_adj', 'Vuln_total_SR_adj']
    # list_financial_sector = DS_file[DS_file['NACE Code'].isin([64, 65, 66])][['EXIOBASE', 'NACE Code']].drop_duplicates()
    # # Filter financial sector and 'Water flow regulation' rows
    # mask = lambda df: df['EXIOBASE'].isin(list_financial_sector['EXIOBASE']) & (df['eco_serv'] == 'Water flow regulation')
    # df_modif = merge.loc[mask(merge), ['EXIOBASE', 'eco_serv'] + cols_to_update]
    # df_orig = DS_file.loc[mask(DS_file), ['EXIOBASE', 'eco_serv'] + cols_to_update]
    # # Compute relative difference
    # relative_diff = (df_modif[cols_to_update] - df_orig[cols_to_update]) / df_orig[cols_to_update]
    # relative_diff.describe().loc[['min', 'mean', 'max']]
    # conclusion: new Vuln are 20 to 50% more important for public sector than when ENCORE value for gov is used
    # option to activate or not
    if config.activation_fin_vuln==1:
        merge = merge_fin_vulnerability(DS_file, List_cntry_sect, config.ratio_Gov_on_NFCpGov)
        DS_file = merge
    #######################################
    # save and store
    #######################################
    # save of DS direct and indirect
    _name = confg_file_name
    if _name.startswith("config_"):
        _name = _name[len("config_"):]
    DS_name = 'DS_' + _name
    DS_file.to_csv(config.path_DS_store +'DS_Vuln_files_stored\\'+ DS_name + '.csv', index=False) # type: ignore
    # DS_file = pd.read_csv(path_DS_store + '/DS_file_20250910.csv')
    # DS_file.head()
    # DS_file.shape
    # DS_file.columns
    #######################################
    # alpha calculation and storage
    #######################################
    Alpha_name = 'Alpha_' + _name
    alpha_calculation( config.data_shock , config.path_DS_store , DS_file , Alpha_name , config.tab_area_country_code )
    return

def ReShape_DS_file(path_DS_store_ , files_name ,isic2nace_raw_path): # files_name = ['config_0_EUshock_10perc.py', 'config_1_EUshock_10perc.py'] ; path_DS_store_ = 'I:\\FS\\FS\\Statsp\\000-Beleidsmedewerkers\\Sebastien Gallet\\Biodiv\\OS-2025\\DS_Vuln_update\\'
    isic2nace_raw = pd.read_csv( isic2nace_raw_path) # isic2nace_raw =config.isic2nace_raw_path
    #######################################
    # DS_file  reshape and files storage
    #######################################
    # identify DS file present in the repertory
    files_name = [f for f in os.listdir(path_DS_store_ + 'DS_Vuln_files_stored\\') if os.path.isfile(os.path.join(path_DS_store_ + 'DS_Vuln_files_stored\\', f))]
    files_name_cleaned = [name for name in files_name if name.startswith('DS_')]
    DS_final = pd.DataFrame()
    for DS_file in files_name_cleaned: # DS_file = 'DS_0_EUshock_10perc.csv'
        DS_raw= pd.read_csv(path_DS_store_ + 'DS_Vuln_files_stored\\' + DS_file)
        DS_shape = DS_raw[['region', 'EXIOBASE', 'eco_serv' , 'DS_total_SR', 'DS_total_max', 'Vuln_total_SR', 'Vuln_total_max' ]].drop_duplicates() # , 'DS_total_max_adj', 'DS_total_SR_adj','Vuln_total_max_adj', 'Vuln_total_SR_adj'
        cleaned_name = DS_file.removeprefix('DS_').removesuffix('.csv')
        target_columns = ['DS_total_SR', 'DS_total_max', 'Vuln_total_SR', 'Vuln_total_max']
        DS_shape.rename(columns={ col: (cleaned_name + '_') + col for col in target_columns}, inplace=True)
        if DS_final.empty :
            DS_final = DS_shape.copy()
        else:
            DS_final = DS_final.merge(DS_shape , on=['region', 'EXIOBASE', 'eco_serv'], how='left')
    # storage
    # add NACE/indout/adj_ind cause always same in every scenarios
    DS_final = DS_final.merge(DS_raw[['region', 'EXIOBASE', 'eco_serv', 'indout', 'NACE Code', 'Adj_ind']], 
                on=['region', 'EXIOBASE', 'eco_serv'], how='left')
    DS_final.to_csv(path_DS_store_ + 'Vuln_final.csv', index=False)
    # for Alpha_ files
    files_name = [f for f in os.listdir(path_DS_store_ + 'DS_Vuln_files_stored\\') if os.path.isfile(os.path.join(path_DS_store_ + 'DS_Vuln_files_stored\\', f))]
    files_name_cleaned = [name for name in files_name if name.startswith('Alpha_')]
    Alpha_final = pd.DataFrame()
    for Alpha_file in files_name_cleaned: # Alpha_file = 'Alpha_1_EUshock_3perc.xlsx'
        Alpha_raw= pd.read_excel(path_DS_store_ + 'DS_Vuln_files_stored\\' + Alpha_file)
        Alpha_shape = Alpha_raw[['Area', 'eco_serv' , 'DS_total_SR_alpha', 'DS_total_max_alpha', 'Vuln_total_SR_alpha', 'Vuln_total_max_alpha' ]].drop_duplicates()
        target_columns = ['DS_total_SR_alpha', 'DS_total_max_alpha', 'Vuln_total_SR_alpha', 'Vuln_total_max_alpha']
        cleaned_name = Alpha_file.removeprefix('Alpha_').removesuffix('.xlsx')
        Alpha_shape.rename(columns={ col: (cleaned_name + '_') + col for col in target_columns}, inplace=True)
        if Alpha_final.empty :
            Alpha_final = Alpha_shape.copy()
        else:
            Alpha_final = Alpha_final.merge(Alpha_shape , on=['Area', 'eco_serv'], how='left')
    # storage
    Alpha_final.to_excel(path_DS_store_ + 'Alpha_final.xlsx', index=False)
    isic2nace_raw[['EXIOBASE','NACE Code']].drop_duplicates().to_excel(path_DS_store_ + 'EXIOBASE_to_NACElvl2_tab.xlsx', index=False) 
    return (Alpha_final.shape, DS_final.shape)

def global_run(path_DS_store_): # path_DS_store_ = path_DS_store
    import importlib.util
    import sys
    #######################################
    # DS_file  calculation and files storage
    #######################################
    # identify DS file present in the repertory
    files_name = [f for f in os.listdir(path_DS_store_ + 'config_store') if os.path.isfile(os.path.join(path_DS_store_ + 'config_store', f))]
    files_name_cleaned = [name[:-3] if name.endswith('.py') else name for name in files_name]
    for config_name in files_name_cleaned: # config_name = 'config_1_EUshock_3perc_08_GOVonNFC'
        os.chdir( path_DS_store_ + 'config_store\\' )
        config = importlib.import_module(config_name)
        DS_file_calculation(path_DS_store_ , config_name) # include alpha calculation
    # reshaoe DS_file and Alpha_file all config_files in two big files: 'Vuln_final.csv' and 'Alpha_final.xlsx'
    ReShape_DS_file(path_DS_store_ , files_name , config.isic2nace_raw_path )
    return

# end of function definition
