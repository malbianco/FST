import os, sys, os.path
from collections import Counter

path='/Users/alberto/Desktop/ALBERTO/DOTTORATO/script/prova_in_corso/'
os.chdir(path)

execfile('input_FST')

print 'You are working in ', path
print
#inputped1=sys.argv[1]

recode={'11':'0','22':'2','12':'1','21':'1','00':'5'}


# Ped number 1
if os.path.exists(path+inputped1):
    print 'File', inputped1, 'read correctly'
else:
    print 'Error !'
    print inputped1, 'does not exist'
    sys.exit()
temp1 = open('geno_temp1','w')
nanim_1 = sum(1 for line in open(inputped1))
with file(inputped1) as f1:
  line1 = f1.readline()
nsnp_1 = ((len(line1.split()))-6)/2
frequenze_1 = [0]*nsnp_1
genotype_1 = [0]*nsnp_1
one = []

# Ped number 2
if os.path.exists(path+inputped2):
    print
    print 'File', inputped2, 'read correctly'
else:
    print 'Error !'
    print inputped2, 'does not exist'
    sys.exit()
temp2 = open('geno_temp2','w')
nanim_2 = sum(1 for line in open(inputped2))
with file(inputped2) as f2:
  line2 = f2.readline()
nsnp_2 = ((len(line2.split()))-6)/2
frequenze_2 = [0]*nsnp_2
genotype_2 = [0]*nsnp_2
two = []

# Map file
if os.path.exists(path+inputmap):
    print
    print 'File', inputmap, 'read correctly'
else:
    print 'Error !'
    print inputmap, 'does not exist'
    sys.exit()

snp_map = sum(1 for line in open(inputmap))
crom = []
snp_name = []
position = []

#########################################
########### Analysis section ############
#########################################
# Working on ped 1
for line in open(inputped1):
    fid_1,ids_1,sire_1,dam_1,sex_1,pheno_1,geno_1=line.strip().split(' ',6)
    geno_1=geno_1.split()
    #for n in range(0,len(geno)):
    genotype_1=[recode.get(geno_1[x]+geno_1[x+1],'!') for x in range(0,len(geno_1)-1,2)]
    temp1.write('%s %s %s\n'%(fid_1,ids_1,' '.join(genotype_1)))
hom1_1 = len([i for i in genotype_1 if i=='0'])
het_1 = len([i for i in genotype_1 if i=='1'])
hom2_1 = len([i for i in genotype_1 if i=='2'])

# Working on ped 2                                                               
for line in open(inputped2):
    fid_2,ids_2,sire_2,dam_2,sex_2,pheno_2,geno_2=line.strip().split(' ',6)
    geno_2=geno_2.split()
    genotype_2=[recode.get(geno_2[x]+geno_2[x+1],'!') for x in range(0,len(geno_2)-1,2)]
    temp2.write('%s %s %s\n'%(fid_2,ids_2,' '.join(genotype_2)))
hom1_2 = len([i for i in genotype_2 if i=='0'])
het_2 = len([i for i in genotype_2 if i=='1'])
hom2_2 = len([i for i in genotype_2 if i=='2'])

# Working on map
snp_number = sum(1 for line in open(inputmap))
crom = []
snp_name = []
position = []

for line in open(inputmap):
    chr,name,cm,pos=line.strip().split()
    crom.append(chr)
    snp_name.append(name)
    position.append(pos)
crom = [int(x) for x in crom]
freq = Counter(crom)

#########################################
######## FST computation section ########
#########################################
snp_dict={}
snp_ord1 = []
snp_ord2 = []
tot = [0]*snp_number
fst = [0]*snp_number

for line in open('map.map'):
    chr,snp,pos1,pos2=line.strip().split()
    snp_dict[snp]=[chr,pos2]
    snp_ord1.append(0)
    snp_ord2.append(0)

# Ped number 1
for line in open('geno_temp1'):
    breed,ids,geno = line.strip().split(' ',2)    
    genos=geno.strip().split()
    for ps,xx in enumerate(genos):
        if xx == '1':
             snp_ord1[ps] +=1

# Ped number 2
for line in open('geno_temp2'):
    breed,ids,geno = line.strip().split(' ',2)
    genos=geno.strip().split()
    for ps,xx in enumerate(genos):
        if xx == '1':
             snp_ord2[ps] +=1

print snp_ord1[0]
print snp_ord2[0]
print 

for x in range(0,len(snp_ord1),1):
    tot[x]=int(snp_ord1[x])+int(snp_ord2[x])

print tot[0]

for x in range(0,len(tot),1):
    fst[x]=round(((tot[x]-snp_ord1[x])/tot[x]),2)
    #round(((float(tot[x]-snp_ord1[x]))/(float(tot[x]))),2)

print fst[0]

sys.exit()

#########################################
############ Results section ############
#########################################
print
print '###########################'
print '####### Statistics  #######'
print '###########################'
print 'Number of animals:'
print fid_1, nanim_1
print fid_2, nanim_2
print 'Number of markers:'
print fid_1, nsnp_1
print fid_2, nsnp_2
print
print 'Map statistics'
for k, v in sorted(freq.items()):
    print 'crom', k, 'number of snp', v
print
print '###########################'
print '##### Frequency table #####'
print '###########################'
print 'Breed =', fid_1, '-', fid_2
print 'hom1 =', round((float(hom1_1)/float(nsnp_1)),2), '-', round((float(hom1_2)/float(nsnp_2)),2)
print 'het =', round((float(het_1)/float(nsnp_1)),2), '-' , round((float(het_2)/float(nsnp_2)),2)
print 'hom2 =', round((float(hom2_1)/float(nsnp_1)),2), '-', round((float(hom2_2)/float(nsnp_2)),2)
print 

if tempfile=='yes':
    print 'Keeping temporary files'
else:
    os.remove('geno_temp1')
    os.remove('geno_temp2') 
    print 'Removing all temporary files'
    print 'If you want save them, please change "tempfile" option'
