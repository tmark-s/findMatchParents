from flask import render_template, request
import os
from app import app

@app.route('/')
def index() :
  return render_template('index.html')

@app.route('/result', methods=['POST'])
def upload_file () :
  c_file = request.files['child']
  c_file.save(os.path.join(app.config['UPLOAD_FOLDER'], c_file.filename))
  print(c_file.filename)

  d_file = request.files['dad']
  d_file.save(os.path.join(app.config['UPLOAD_FOLDER'], d_file.filename))
  print(d_file.filename)

  m_file = request.files['mom']
  m_file.save(os.path.join(app.config['UPLOAD_FOLDER'], m_file.filename))
  print(m_file.filename)

  c = c_file.filename.split(".")
  d = d_file.filename.split(".")
  m = m_file.filename.split(".")

  ######################################################## INPUT FILE ######################################################## 
  child = c[0]
  dad = d[0]
  mom = m[0]
  depth = 50
  ######################################################## INPUT FILE ######################################################## 





  ######################################################## METHOD ######################################################## 
  #remove metadata or chrM
  def removeMetadata (data) :
      dataWithoutMetaOrChrM = []
      for i in range(len(data)) :
          if data[i][0] != "#" and data[i][3] != "M" :
              dataWithoutMetaOrChrM.append(data[i])
      return dataWithoutMetaOrChrM

  #remove chrX or chrY
  def removeChrXOrY (data) :
      dataWithoutChrXOrY = []
      for i in range(len(data)) :
          if data[i][3] != "X" and data[i][3] != "Y" :
              dataWithoutChrXOrY.append(data[i])
      return dataWithoutChrXOrY

  #keep data before included (delete chr)
  def preparedData (data) :
      dataPrepared = []
      for i in range(len(data)) :
          x = data[i].split()
          y = x[0]
          x[0] = y[3:len(y)]
          dataPrepared.append(data[i][3:len(data[i])])
      return dataPrepared

  #keep data in dict format
  def convertToDict (data) :
      dataDict = {}
      for i in range(len(data)) :
          x = data[i].split()
          y = x[0] + "_" + x[1]
          dataDict[y] = data[i]
      return dataDict

  #find  REF allele
  def findREF (data) :
      x = data.split()
      return x[3]

  #find ALT allele
  def findALT (data) :
      x = data.split()
      return x[4]

  #find FILTER
  def findFilter (data) :
      x = data.split()
      return x[6]

  #find GT
  def findGT (data) :
      x = data.split()
      y = x[9].split(":")
      return y[0]

  #find DP
  def findDP (data) :
      x = data.split()
      y = x[7].split(";")
      for i in range(len(y)) :
          z = y[i].split("=")
          if z[0] == "DP" :
              return z[1]

  #find AD
  def findAD (data) :
      x = data.split()
      y = x[9].split(":")
      return y[1]
  ######################################################## METHOD ########################################################





  ######################################################## READ CHILD DAD MOM FILE ########################################################
  ########## CHILD ########## 
  #read child vcf file
  child_file = open("./uploads/" + child + ".vcf","r")
  child_data = []
  for line in child_file:
      child_data.append(line)
  child_file.close()

  #remove metadata or chrM of child file
  child_dataWithoutMetaOrChrM = removeMetadata(child_data)

  #remove chrX or chrY of child file
  child_dataWithoutChrXOrY = removeChrXOrY(child_dataWithoutMetaOrChrM)

  #keep data before included of child file
  child_dataPrepared = preparedData(child_dataWithoutChrXOrY)
  ########## CHILD ########## 



  ########## DAD ##########
  #read dad vcf file
  dad_file = open("./uploads/" + dad + ".vcf","r")
  dad_data = []
  for line in dad_file:
      dad_data.append(line)
  dad_file.close()

  #remove metadata or chrM of dad file
  dad_dataWithoutMetaOrChrM = removeMetadata(dad_data)

  #remove chrX or chrY of dad file
  dad_dataWithoutChrXOrY = removeChrXOrY(dad_dataWithoutMetaOrChrM)

  #keep data before included of dad file
  dad_dataPrepared = preparedData(dad_dataWithoutChrXOrY)
  ########## DAD ##########



  ########## MOM ##########
  #read mom vcf file
  mom_file = open("./uploads/" + mom + ".vcf","r")
  mom_data = []
  for line in mom_file:
      mom_data.append(line)
  mom_file.close()

  #remove metadata or chrM of mom file
  mom_dataWithoutMetaOrChrM = removeMetadata(mom_data)

  #remove chrX or chrY of mom file
  mom_dataWithoutChrXOrY = removeChrXOrY(mom_dataWithoutMetaOrChrM)

  #keep data before included of mom file
  mom_dataPrepared = preparedData(mom_dataWithoutChrXOrY)
  ########## MOM ##########
  ######################################################## READ CHILD DAD MOM FILE ########################################################





  ######################################################## FIND ALL POSITION ########################################################
  chrPos = []
  ########## CHILD ##########
  for i in range(len(child_dataPrepared)) :
      x = child_dataPrepared[i].split()
      pair = (int(x[0]),int(x[1]))
      chrPos.append(pair)
  ########## CHILD ##########



  ########## DAD ##########
  for i in range(len(dad_dataPrepared)) :
      x = dad_dataPrepared[i].split()
      pair = (int(x[0]),int(x[1]))
      chrPos.append(pair)
  ########## DAD ##########



  ########## MOM ##########
  for i in range(len(mom_dataPrepared)) :
      x = mom_dataPrepared[i].split()
      pair = (int(x[0]),int(x[1]))
      chrPos.append(pair)
  ########## MOM ##########



  chrPos = set(chrPos)
  chrPos = list(chrPos)
  chrPos = sorted(chrPos)
  ######################################################## FIND ALL POSITION ########################################################





  ######################################################## CREATE DICT ########################################################
  child_dataDict = convertToDict(child_dataPrepared)
  dad_dataDict = convertToDict(dad_dataPrepared)
  mom_dataDict = convertToDict(mom_dataPrepared)
  ######################################################## CREATE DICT ######################################################## 





  ######################################################## WRITE NEW FILE ######################################################## 
  file = open("./uploads/" + child + "," + dad + "," + mom + ".vcf","w")
  for i in range(len(chrPos)) :
      chrom = str(chrPos[i][0])
      pos = str(chrPos[i][1])
      find = chrom + "_" + pos

      #child
      if find in child_dataDict.keys() :
          file.write("chr" + chrom + "\t" + pos + "\t" + findREF(child_dataDict[find]) + "\t" + findALT(child_dataDict[find]) + "\t" + findFilter(child_dataDict[find]) + "\t" + str(findGT(child_dataDict[find])) + "\t" + str(findDP(child_dataDict[find])) + "\t" + str(findAD(child_dataDict[find])))
      else :
          file.write("chr" + chrom + "\t" + pos + "\t" + "." + "\t" + "." + "\t" + "." + "\t" + "0/0" + "\t" + "0" + "\t" + "0,0")

      #dad
      if find in dad_dataDict.keys() :
          file.write("\t" + findREF(dad_dataDict[find]) + "\t" + findALT(dad_dataDict[find]) + "\t" + findFilter(dad_dataDict[find]) + "\t" + str(findGT(dad_dataDict[find])) + "\t" + str(findDP(dad_dataDict[find])) + "\t" + str(findAD(dad_dataDict[find])))
      else :
          file.write("\t" + "." + "\t" + "." + "\t" + "." + "\t" + "0/0" + "\t" + "0" + "\t" + "0,0")

      #mom
      if find in mom_dataDict.keys() :
          file.write("\t" + findREF(mom_dataDict[find]) + "\t" + findALT(mom_dataDict[find]) + "\t" + findFilter(mom_dataDict[find]) + "\t" + str(findGT(mom_dataDict[find])) + "\t" + str(findDP(mom_dataDict[find])) + "\t" + str(findAD(mom_dataDict[find])))
      else :
          file.write("\t" + "." + "\t" + "." + "\t" + "." + "\t" + "0/0" + "\t" + "0" + "\t" + "0,0")

      file.write("\n")
  file.close()
  ######################################################## WRITE NEW FILE ########################################################





  ######################################################## READ NEW CREATED FILE ########################################################
  new_file = open("./uploads/" + child + "," + dad + "," + mom + ".vcf","r")
  data_in_file = []
  for line in new_file :
      data_in_file.append(line)
  new_file.close()
  ######################################################## READ NEW CREATED FILE ########################################################





  ######################################################## REMOVE FILTER != PASS ########################################################
  dataWithFilterPASS = []
  for i in range(len(data_in_file)) :
      x = data_in_file[i].split()
      if ((x[4] == 'PASS' or x[4] == '.') and (x[10] == 'PASS' or x[10] == '.') and (x[16] == 'PASS' or x[16] == '.')) :
          dataWithFilterPASS.append(data_in_file[i])
  print(len(dataWithFilterPASS))
  ######################################################## REMOVE FILTER != PASS ########################################################





  ######################################################## REMOVE SNV ########################################################
  dataWithoutSNV = []
  for i in range(len(dataWithFilterPASS)) :
      x = dataWithFilterPASS[i].split()
      y1 = len(x[2])
      y2 = len(x[3])
      y3 = len(x[8])
      y4 = len(x[9])
      y5 = len(x[14])
      y6 = len(x[15])
      if (y1 == 1 and y2 == 1 and y3 == 1 and y4 == 1 and y5 == 1 and y6 == 1) :
          dataWithoutSNV.append(dataWithFilterPASS[i])
  print(len(dataWithoutSNV))
  ######################################################## REMOVE SNV ########################################################





  ######################################################## DELETE DATA WITH DP < 50 ########################################################
  dataWithDPGreaterThan50 = []
  for i in range(len(dataWithoutSNV)) :
      x = dataWithoutSNV[i].split()
      if (int(x[6]) >= depth or int(x[6]) == 0) and (int(x[12]) >= depth or int(x[12]) == 0) and (int(x[18]) >= depth or int(x[18]) == 0) :
          dataWithDPGreaterThan50.append(dataWithoutSNV[i])
  print(len(dataWithDPGreaterThan50))
  ######################################################## DELETE DATA WITH DP < 50 ########################################################





  ######################################################## DELETE DATA WITH AD < 10% ########################################################
  dataWithFilterAD_child = []
  for i in range(len(dataWithDPGreaterThan50)) :
      x = dataWithDPGreaterThan50[i].split()
      y1 = x[7].split(",")
      if (x[5] == '0/1') :
          if (float(y1[1]) != 0.0 and float(y1[0])/(float(y1[0])+float(y1[1])) >= 0.1) :
              dataWithFilterAD_child.append(dataWithDPGreaterThan50[i])
      elif (x[5] == '1/1') :
          if (float(y1[1]) != 0.0 and float(y1[0])/(float(y1[0])+float(y1[1])) < 0.1) :
              dataWithFilterAD_child.append(dataWithDPGreaterThan50[i])
      elif (x[5] == '0/0') :
          dataWithFilterAD_child.append(dataWithDPGreaterThan50[i])

  dataWithFilterAD_dad = []
  for i in range(len(dataWithFilterAD_child)) :
      x = dataWithFilterAD_child[i].split()
      y2 = x[13].split(",")
      if (x[11] == '0/1') :
          if (float(y2[1]) != 0.0 and float(y2[0])/(float(y2[0])+float(y2[1])) >= 0.1) :
              dataWithFilterAD_dad.append(dataWithFilterAD_child[i])
      elif (x[11] == '1/1') :
          if (float(y2[1]) != 0.0 and float(y2[0])/(float(y2[0])+float(y2[1])) < 0.1) :
              dataWithFilterAD_dad.append(dataWithFilterAD_child[i])
      elif (x[11] == '0/0') :
          dataWithFilterAD_dad.append(dataWithFilterAD_child[i])

  dataWithFilterAD_mom = []
  for i in range(len(dataWithFilterAD_dad)) :
      x = dataWithFilterAD_dad[i].split()
      y3 = x[19].split(",")
      if (x[17] == '0/1') :
          if (float(y3[1]) != 0.0 and float(y3[0])/(float(y3[0])+float(y3[1])) >= 0.1) :
              dataWithFilterAD_mom.append(dataWithFilterAD_dad[i])
      elif (x[17] == '1/1') :
          if (float(y3[1]) != 0.0 and float(y3[0])/(float(y3[0])+float(y3[1])) < 0.1) :
              dataWithFilterAD_mom.append(dataWithFilterAD_dad[i])
      elif (x[17] == '0/0') :
          dataWithFilterAD_mom.append(dataWithFilterAD_dad[i])

  print(len(dataWithFilterAD_mom))
  ######################################################## DELETE DATA WITH AD < 10% ########################################################





  ######################################################## WRITE FILE WITH DP > 50 and AD > 10% ########################################################
  write_new_file = open("./uploads/" + child + "," + dad + "," + mom + ".vcf","w")
  write_new_file.write("#CHROM" + "\t" + "POS" + "\t" + "REF" + "\t" + "ALT" + "\t" + child + "\t" + "DP" + "\t" + "AD" + "\t" + dad + "\t" + "DP" + "\t" + "AD" + "\t" + mom + "\t" + "DP" + "\t" + "AD" + "\n")
  for i in range(len(dataWithFilterAD_mom)) : 
      x = dataWithFilterAD_mom[i].split()
      write_new_file.write(x[0] + "\t" + x[1] + "\t" + x[2] + "\t" + x[3] + "\t" + x[5] + "\t" + x[6] + "\t" + x[7] + "\t" + x[11] + "\t" + x[12] + "\t" + x[13] + "\t" + x[17] + "\t" + x[18] + "\t" + x[19])
      write_new_file.write("\n")
  write_new_file.close()
  ######################################################## WRITE FILE WITH DP > 50 and AD > 10% ########################################################





  ######################################################## CAL INFORMATIVE, UNINFORMATIVE AND MISMATCH ########################################################
  #read vcf file
  open_file = open("./uploads/" + child + "," + dad + "," + mom + ".vcf","r")
  data = []
  for line in open_file :
      if line[0] != '#' :
          data.append(line)
  file.close()

  #initial value
  informative = 0
  uninformative = 0
  mismatch = 0

  #count
  for i in range(len(data)) :
      x = data[i].split()
      if x[4] == '0/0' :
          if x[7] == '0/0' :
              if x[10] == '0/0' :
                  uninformative += 1
              elif x[10] == '0/1' :
                  informative += 1
              elif x[10] == '1/1' :
                  mismatch += 1
          elif x[7] == '0/1' :
              if x[10] == '0/0' :
                  informative += 1
              elif x[10] == '0/1' :
                  informative += 1
              elif x[10] == '1/1' :
                  mismatch += 1
          elif x[7] == '1/1' :
              if x[10] == '0/0' :
                  mismatch += 1
              elif x[10] == '0/1' :
                  mismatch += 1
              elif x[10] == '1/1' :
                  mismatch += 1
      elif x[4] == '0/1' :
          if x[7] == '0/0' :
              if x[10] == '0/0' :
                  mismatch += 1
              elif x[10] == '0/1' :
                  informative += 1
              elif x[10] == '1/1' :
                  informative += 1
          elif x[7] == '0/1' :
              if x[10] == '0/1' :
                  uninformative += 1
              elif x[10] == '0/0' :
                  informative += 1
              elif x[10] == '1/1' :
                  informative += 1
          elif x[7] == '1/1' :
              if x[10] == '1/1' :
                  mismatch += 1
              elif x[10] == '0/0' :
                  informative += 1
              elif x[10] == '0/1' :
                  informative += 1
      elif x[4] == '1/1' :
          if x[7] == '0/0' :
              if x[10] == '0/0' :
                  mismatch += 1
              elif x[10] == '0/1' :
                  mismatch += 1
              elif x[10] == '1/1' :
                  mismatch += 1
          elif x[7] == '0/1' :
              if x[10] == '0/0' :
                  mismatch += 1
              elif x[10] == '0/1' :
                  informative += 1
              elif x[10] == '1/1' :
                  informative += 1
          elif x[7] == '1/1' :
              if x[10] == '0/0' :
                  mismatch += 1
              elif x[10] == '0/1' :
                  informative += 1
              elif x[10] == '1/1' :
                  uninformative += 1

  total = len(data)

  print(child + " " + dad + " " + mom)
  print("total = " + str(total))
  print("informative = " + str(informative))
  print("uninformative = " + str(uninformative))
  print("mismatch = " + str(mismatch))

  percentInformative = round((informative/total)*100, 2)
  percentUninformative = round((uninformative/total)*100, 2)
  percentMismatch = round((mismatch/total)*100, 2)
  
  os.remove("./uploads/" + child + ".vcf")
  os.remove("./uploads/" + dad + ".vcf")
  os.remove("./uploads/" + mom + ".vcf")
  os.remove("./uploads/" + child + "," + dad + "," + mom + ".vcf")
  ######################################################## CAL INFORMATIVE, UNINFORMATIVE AND MISMATCH ########################################################

  return render_template('result.html', percentInformative = percentInformative, percentUninformative = percentUninformative, percentMismatch = percentMismatch)