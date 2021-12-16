from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.core import serializers
from Ad.views import deleteAd
from PFE.models import User,Ad,Campus,Location,Media,Category,AdsCampusLocation
import json

def login(request):

    if request.method == 'POST':
        j = json.loads(request.body.decode())
        user = User(**j)
        #print(serializers.serialize(User.objects.all()))
        res = User.objects.filter(email=user.email,password=user.password)
        print(res)
        token = Token.generate_key()  # Token.objects.create(user=res.first().firstname)
        if(res.count() != 0):
            return HttpResponse(content=json.dumps({"token": token, "user": {"firstname": res.first().firstname, "lastname": res.first().lastname,"id":res.first().id}}), content_type="application/json")
        else:
            return HttpResponse(status=404)
    else:
        return HttpResponse(status=400)

def register(request):
    if request.method == 'POST':
        j = json.loads(request.body.decode())
        print(request.body)
        user = User(email=j["email"],lastname = j["lastname"],firstname =j["firstname"],campus = Campus.objects.get(pk=j["campus"]), password=j["password"], moderator=j["moderator"])
        try:
            # print(j)
            user.save()
            res = User.objects.last()        
            print('new id : ')
            print(res.id)
            token = Token.generate_key()
            return HttpResponse(content=json.dumps({"token": token, "user": {"firstname": res.firstname, "lastname":  res.lastname,"id":res.id}}), content_type="application/json")
        except:
            return HttpResponse(status=409)    
    else:
        return HttpResponse(status=400)

def getUserById(request, id):
    if request.method == 'GET':
        try:
            print(id)
            j = User.objects.get(pk=id)
            print(j.campus)
            user = serializers.serialize('json', [j], ensure_ascii=False)
            campus=j.campus
            joined = f",\"campusName\":\"{campus.campusName}\" }}]".join(user.split('}]'))

            return HttpResponse(joined, content_type='txt', status=200)
        except:
          return HttpResponse(status=500)
    else:
        return HttpResponse(status=400)


def getAllUsers(request):
    if request.method == 'GET':
        try:
            users = User.objects.all()
            users = serializers.serialize('json', users, ensure_ascii=False)
            print(users)
            return HttpResponse(users, content_type='application.json', status=200) 
        except:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=400)
  
        

def editUser(request, id):
    if request.method == 'PUT':
        try:
            idUser=id
            newData = json.loads(request.body.decode())
            print("---------",newData)
            User.objects.filter(id=idUser).update(campus=2)
            print("---------")
            print("old campus : ",User.objects.filter(id=idUser)[0].id)

            if newData['campus'] != '':
                newCampus=Campus.objects.filter(campusName=newData['campus'])[0].id
                print(newCampus)
                User.objects.filter(pk=id).update(campus=newCampus)
                
            if newData['password'] != '':
                User.objects.filter(pk=id).update(password=newData['password'])
            print('Updated')
            response_data = 'User updated'
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)
        except:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=400)
   
def deleteUser(request, id):
    if request.method == 'DELETE':
        try:
            if User.objects.filter(pk=id):
                print('delete user id')
                print(id)
                adsToDelete = Ad.objects.filter(seller=id).values_list()
                adsIdList=[]
                for index in range(adsToDelete.count()):
                    adsIdList.append(adsToDelete[index][0])

                print(adsIdList)
        
                for index in range(len(adsIdList)):
                    print('ad id :')
                    deleteAd([],adsIdList.pop())
                
                User.objects.filter(pk=id).delete()
                response_data = 'user deleted'
                return HttpResponse(json.dumps(response_data),content_type='applicatoin/json',status=200)
            else:
             print('User not found')
             return HttpResponse(status=404)
        except:
            return HttpResponse(status = 500)
    else:
        return HttpResponse(status=400)
    

# Test function
def Hello(request):
    return HttpResponse("Welcome Backend")
    

#Insert dummy data
def insertTestData(request):

    #-------------------------------------The campus and the sites--------------------------------------------------#
    Ixelles = Campus(campusName='Ixelles')
    Ixelles.save()
    WA249 = Location(name='Wavre_249', address='Chaussée de Wavre,249', campus = Ixelles )
    LI14 = Location(name='Limauge_14',address='Rue de Limauge,14',campus = Ixelles)
    AR = Location(name = 'Arlon', address='Rue d\'Arlon 3-5-11,4-6-14',campus = Ixelles)
    TR84 = Location(name='TRËVE_84',address='Rue de Trêve,84/Rue d\'Arlon,53',campus = Ixelles)
    WA249.save()
    LI14.save()
    AR.save()
    TR84.save()

    woluwe = Campus(campusName='Woluwe')
    woluwe.save()

    AL= Location(name='ALMA_II',address='Place de l\'Alma 3')
    ARC59= Location(name='ARCHES',address='Promenade de l\'Alma,59')
    CH41= Location(name='CHAMPS_41',address='Clos Chappelle-aux-Champs,41')
    CH43= Location(name='CHAMPS_43',address='Clos Chappelle-aux-Champs,43')
    MO84= Location(name='MOUNIER_84',address='Avenue Emmanuel Mounier,84')
    AL.save()
    ARC59.save()
    CH41.save()
    CH43.save()
    MO84.save()

    louvain = Campus(campusName='Louvain-La-Neuve')
    louvain.save()

    BA17 = Location(name='BARDANE_17',address='Chemin de la Bardane_27',campus=louvain)
    CA1 = Location(name='CARDLIJN_10',address='Voie Cardlijn,10',campus=louvain)
    LO1 = Location(name='LOVANO_1',address='Rue du traité de Rome,1',campus=louvain)
    LO14 = Location(name='LOVANO_14',address='Rue Pauline Ladeuze,14',campus=louvain)
    UE4 = Location(name='UNION EUROPEENE_4',address='Rue du traité de Rome,1',campus=louvain)

    BA17.save()
    CA1.save()
    LO14.save()
    LO1.save()
    UE4.save()
    #------------------------------------------------------------------------------------------------------------------------------#

    #--------------------------------------------------------Categories--------------------------------------------------------------#
    maisonJardin = Category(categoryName='Maison et Jardin')
    maisonJardin.save() #1
    outils = Category(categoryName='Outils',parent=maisonJardin)
    meubles = Category(categoryName='Meubles',parent=maisonJardin)
    pourMaison = Category(categoryName='Pour la maison',parent=maisonJardin)
    jardin = Category(categoryName='Jardins',parent=maisonJardin)
    electro = Category(categoryName='Electroménager',parent=maisonJardin)
    outils.save() #2
    meubles.save() #3
    pourMaison.save() #4
    jardin.save() #5
    electro.save() #6

    famille = Category(categoryName='Famille')
    famille.save() #7
    sante = Category(categoryName='Santé et beauté',parent=famille)
    fournitures = Category(categoryName='Fournitures pour animaux',parent=famille)
    puericulture = Category(categoryName='Puériculture et enfants',parent=famille)
    jeux = Category(categoryName='Jouets et jeux',parent=famille)
    sante.save() #8
    fournitures.save() #9
    puericulture.save() #10
    jeux.save() #11

    vetement = Category(categoryName='Vêtements et accessoires')
    vetement.save() #12
    femme = Category(categoryName='Vêtements et chaussures femmes',parent=vetement)
    homme = Category(categoryName='Vêtements et chaussures hommes',parent=vetement)
    bijoux = Category(categoryName='Bijoux et accessoires',parent=vetement)
    sacs = Category(categoryName='Sacs et bagages',parent=vetement)
    femme.save() #13
    homme.save() #14
    bijoux.save() #15
    sacs.save() #16

    loisir= Category(categoryName='Loisirs - hobbys')
    loisir.save() #17
    velo = Category(categoryName = 'Vélo',parent=loisir)
    creatif = Category(categoryName='Loisir créatifs',parent=loisir)
    pieces = Category(categoryName='Piéces auto',parent=loisir)
    sports = Category(categoryName='Sports et activités d\'extérieures',parent=loisir)
    jeuxVideo = Category(categoryName='Jeux vidéo',parent=loisir)
    livres = Category(categoryName='Livres,films et musique',parent=loisir)
    instruments = Category(categoryName='Instruments de musique',parent=loisir)
    antiquite = Category(categoryName='Antiquité et objets de collection',parent=loisir)
    velo.save() #18
    creatif.save() #19
    pieces.save() #20
    sports.save() #21
    jeuxVideo.save() #22
    livres.save() #23
    instruments.save() #24
    antiquite.save() #25

    Electro = Category(categoryName='Electronique')
    Electro.save() #26
    ordi=Category(categoryName='Electronique et ordinateurs',parent=Electro)
    tele=Category(categoryName='Téléphones mobiles',parent=Electro)
    ordi.save() #27
    tele.save() #28
     #------------------------------------------------------------------------------------------------------------------------------#


    #-------------------------------------------------------------Users--------------------------------------------------------------#
    chihhuai = User(email='chihhuai.lin@student.vinci.be',lastname = 'Lin',firstname ='Chih Huai',campus = louvain, password='123', moderator=False)
    abdulhmid = User(email='abdulhamid.ali@student.vinci.be',lastname = 'Ali',firstname ='Abdulhamid',campus = Ixelles, password='123', moderator=False)
    ikram = User(email='ikrambouali24@student.vinci.be',lastname = 'Bouali',firstname ='Ikram',campus = Ixelles, password='123', moderator=False)
    admin = User(email='admin@vinci.be',lastname = 'admin',firstname ='admin',campus = woluwe, password='admin123', moderator=True)
    chihhuai.save()   
    abdulhmid.save()
    ikram.save()
    admin.save()
     #---------------------------------------------------------------------------------------------------------------------------------#


      #---------------------------------------------------------Advertisements---------------------------------------------------------------#
    tshirt = Ad(status = Ad.Status.TOGIVE, title ='T-shirt', description= 'porté une seule fois',price = 0,category=homme, seller = chihhuai)
    bike = Ad(status = Ad.Status.TOSELL, title ='Vélo', description= 'vélo pour adulte rose',price = 55,category=velo, seller = chihhuai)
    furniture = Ad(status = Ad.Status.TOSELL, title ='Meuble salon', description= 'armoire de rangement',price = 35,category=meubles, seller = chihhuai)
    harryPotter = Ad(status = Ad.Status.TOGIVE, title ='Harry Potter Tome 4', description= 'harry potter et la coupe de feu',price = 0,category=livres, seller = chihhuai)
    ps4Game = Ad(status = Ad.Status.TOSELL, title ='Jeux ps4', description= 'vend plusieurs jeux ps4',price = 10,category=jeuxVideo, seller = abdulhmid)
    cam = Ad(status = Ad.Status.TOSELL, title ='Appareil photo', description= 'état neuf marque Fujifilm',price = 350,category=creatif, seller = abdulhmid)
    parfum = Ad(status = Ad.Status.TOSELL, title ='Parfum Zara', description= 'Parfum Zara neuf jamais ouvert',price = 5,category=sante, seller = abdulhmid)

    TV = Ad(status = Ad.Status.TOSELL, title ='TV samsumg', description= 'HD 32 pouces, tv noir',price = 55,category=pourMaison, seller = abdulhmid)
    backpack = Ad(status = Ad.Status.TOSELL, title ='Sac à dos Ralp Lauren', description= 'Sac à dos Ralph Lauren neuf jamais porté offert par ma grand-mère',price = 87,category=sacs, seller = abdulhmid)
    vase = Ad(status = Ad.Status.TOSELL, title ='Vase chinois', description= 'Vase chinois émaux cloisonnés très joli ',price = 199,category=pourMaison, seller = abdulhmid)
    highheels = Ad(status = Ad.Status.TOSELL, title ='Talons transparents', description= 'Talons transparents taille 37 jamais portés avec étiquette',price = 45,category=femme, seller = ikram)
    goldorak = Ad(status = Ad.Status.TOSELL, title ='Goldorak ', description= 'Figurine Goldorak de 60 cm + Figurine mini métal + le nouveau livre .',price = 700,category=jeux, seller = ikram)
    jordan = Ad(status = Ad.Status.TOSELL, title ='Jordan', description= 'Jordan taille 42 neuves avec étiquette',price = 150,category=vetement, seller = ikram)
    iphone = Ad(status = Ad.Status.TOSELL, title ='iphone', description= 'iphone 13 pro',price = 300,category=tele, seller = ikram)
    bracelet = Ad(status = Ad.Status.TOSELL, title ='Bracelet', description= 'Bracelet labradorite et cristal de roche',price = 18,category=bijoux, seller = ikram)
     
    tshirt.save() 
    bike.save()
    furniture.save()
    harryPotter.save()
    ps4Game.save()
    cam.save()

    TV.save()
    backpack.save()
    vase.save()
    highheels.save()
    goldorak.save()
    jordan.save()
    iphone.save()
    bracelet.save()
     #----------------------------------------------------------AdsCampusLocation--------------------------------------------------------------#
    adcampLocTshirt = AdsCampusLocation(ad=tshirt,campus=woluwe,location=AL)
    adcampLocBike = AdsCampusLocation(ad=bike,campus=Ixelles,location=WA249)
    adcampLocFurniture = AdsCampusLocation(ad=furniture,campus=louvain,location=BA17)
    adcampLocHarry = AdsCampusLocation(ad=harryPotter,campus=woluwe,location=CH43)
    adcampLocPS4 = AdsCampusLocation(ad=ps4Game,campus=Ixelles,location=LI14)
    adcampLocCam = AdsCampusLocation(ad=cam,campus=louvain,location=CA1)
    adcampLocParfum = AdsCampusLocation(ad=parfum,campus=woluwe,location=AL)
    adcampLocTV = AdsCampusLocation(ad=TV,campus=woluwe,location=ARC59)
    adcampLocBackpack = AdsCampusLocation(ad=backpack,campus=woluwe,location=CH41)
    adcampLocVase = AdsCampusLocation(ad=vase,campus=Ixelles,location=AR)
    adcampLocHighHeel = AdsCampusLocation(ad=highheels,campus=louvain,location=UE4)
    adcampLocGoldorak = AdsCampusLocation(ad=goldorak,campus=Ixelles,location=TR84)
    adcampLocJordan = AdsCampusLocation(ad=jordan,campus=louvain,location=LO14)
    adcampLocIphone = AdsCampusLocation(ad=iphone,campus=woluwe,location=CH41)
    adcampLocBracelet = AdsCampusLocation(ad=bracelet,campus=woluwe,location=MO84)

   
    adcampLocTshirt.save()
    adcampLocBike.save()
    adcampLocFurniture.save()
    adcampLocHarry.save()
    adcampLocPS4.save()
    adcampLocTV.save()
    adcampLocParfum.save()
    adcampLocBackpack.save()
    adcampLocVase.save()
    adcampLocHighHeel.save()
    adcampLocGoldorak.save()
    adcampLocJordan.save()
    adcampLocIphone.save()
    adcampLocBracelet.save()
    adcampLocCam.save()
     #---------------------------------------------------------------------------------------------------------------------------------#
    
     #---------------------------------------------------------Media--------------------------------------------------------------------#
    meTshirt = Media(url='https://i.ibb.co/LN5Z7qP/tshirt.jpg',ad=tshirt)
    meBike = Media(url='https://i.ibb.co/Cs8pwxp/velo.jpg',ad=bike)
    meFurniture = Media(url='https://i.ibb.co/vq1TK28/meuble.jpg',ad=furniture)
    meHarry1 = Media(url='https://i.ibb.co/GQnCVBS/fp.png',ad=harryPotter)
    meHarry2 = Media(url='https://i.ibb.co/vzmWnrj/HP4.jpg',ad=harryPotter)

    mePS41 = Media(url='https://i.ibb.co/VYbHVxB/ps1.jpg',ad=ps4Game)
    mePS42 = Media(url='https://i.ibb.co/MCqtMXr/ps2.jpg',ad=ps4Game)

    meTV1 = Media(url='https://i.ibb.co/Smn535t/gg.png',ad=TV)
    meTV2 = Media(url='https://i.ibb.co/LPrq7pv/tv.png',ad=TV)
    meTV3 = Media(url='https://i.ibb.co/TL57Khf/hh.png',ad=TV)

    meCam1 = Media(url='https://i.ibb.co/r6HnDmh/ca1.jpg',ad=cam)
    meCam2 = Media(url='https://i.ibb.co/Krbg1Zh/ca2.jpg',ad=cam)
    meCam3 = Media(url='https://i.ibb.co/BykvBZz/ca3.jpg',ad=cam)


    meBackpack = Media(url='https://i.ibb.co/MhNLSp5/1639474071.jpg',ad=backpack)

    meVase1 = Media(url='https://i.ibb.co/zGvFHjz/5555.jpg',ad=vase)
    meVase2 = Media(url='https://i.ibb.co/0Zf3R6j/16379164555.jpg',ad=vase)
    meVase3 = Media(url='https://i.ibb.co/jbzRKV0/1637916455.jpg',ad=vase)

    meHighHeel = Media(url='https://i.ibb.co/wc5BTJj/1639557305.jpg',ad=highheels)

    meGoldorak = Media(url='https://i.ibb.co/d2W28Jq/1639507754.jpg',ad=goldorak)

    meJordan1 = Media(url='https://i.ibb.co/w60HWpc/1639425523.jpg',ad=jordan)
    meJordan2 = Media(url='https://i.ibb.co/k27dXPV/16394255234.jpg',ad=jordan)
    meJordan3 = Media(url='https://i.ibb.co/m9V9yqP/16394255233.jpg',ad=jordan)
    meJordan4 = Media(url='https://i.ibb.co/PNSGzKV/16394255231.jpg',ad=jordan)

    meParfum = Media(url='https://i.ibb.co/V3fcsqR/1639580926161.jpg',ad=parfum)

    meIphone =Media(url='https://i.ibb.co/Mck561W/1639498845.jpg',ad=iphone)
     
    meTshirt.save()
    meFurniture.save()
    meBike.save()
    meHarry1.save()
    meHarry2.save()
    mePS41.save()
    mePS42.save()
    meTV1.save()
    meTV2.save()
    meTV3.save()
    meCam1.save()
    meCam2.save()
    meCam3.save()
    meBackpack.save()
    meVase1.save()
    meVase2.save()
    meVase3.save()
    meHighHeel.save()
    meGoldorak.save()
    meParfum.save()
    meJordan1.save()
    meJordan2.save()
    meJordan3.save()
    meJordan4.save()
    meIphone.save()

    return HttpResponse('Some stuff got added in the db')