from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.http import HttpResponse
from django.core import serializers
from Ad.views import deleteAd
from PFE.models import AdsCampusLocation, User,Ad,Campus,Location,Media,Category
import json

def login(request):

    if request.method == 'POST':
        j = json.loads(request.body.decode())
        user = User(**j)
        res = User.objects.filter(email=user.email)
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
          response_data = "test-register"
          return HttpResponse(json.dumps(response_data), content_type="application/json", status=200)
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
            print(id)
            newData = json.loads(request.body.decode())
            if newData['campus'] != '':
                User.objects.filter(pk=id).update(campus=newData['campus'])
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
                    deleteAd('http://127.0.0.1:8000/ads/delete/',adsIdList.pop())
                
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

    #The campus and the sites
    Ixelles = Campus(campusName='Ixelles')
    Ixelles.save()
    WA249 = Location(name='Wavre_249', address='Chaussée de Wavre,249' )
    LI14 = Location(name='Limauge_14',address='Rue de Limauge,14')
    AR = Location(name = 'Arlon', address='Rue d\'Arlon 3-5-11,4-6-14')
    TR84 = Location(name='TRËVE_84',address='Rue de Trêve,84/Rue d\'Arlon,53')
    WA249.save()
    LI14.save()
    AR.save()
    TR84.save()

    woluwe = Campus(campusName='Woluwe')
    woluwe.save()
    AL= Location(name='ALMA_II',address='Place de l\'Alma 3')
    ARC59= Location(name='ARCHES',address='Promenade de l\'Alma,59')
    CH41= Location(name='CHAMPS_41',address='Clos Chappelle-aux-Champs,41')
    CH42= Location(name='CHAMPS_43',address='Clos Chappelle-aux-Champs,43')
    MO84= Location(name='MOUNIER_84',address='Avenue Emmanuel Mounier,84')
    AL.save()
    ARC59.save()
    CH41.save()
    CH42.save()
    MO84.save()

    louvain = Campus(campusName='Louvain la Neuve')
    louvain.save()

    BA17 = Location(name='BARDANE_17',address='Chemin de la Bardane_17')
    CA1 = Location(name='CARDLIJN_10',address='Voie Cardlijn,10')
    LO1 = Location(name='LOVANO_1',address='Rue du traité de Rome,1')
    LO14 = Location(name='LOVANO_14',address='Rue Pauline Ladeuze,14')
    UE4 = Location(name='UNION EUROPEENE_4',address='Rue du l\'Union Européene,4')

    BA17.save()
    CA1.save()
    LO14.save()
    LO1.save()
    UE4.save()

    #Categories

    outils = Category(categoryName='Outils')
    meubles = Category(categoryName='Meubles')
    pourMaison = Category(categoryName='Pour la maison')
    jardin = Category(categoryName='Jardins')
    electro = Category(categoryName='Electroménager')
    outils.save()
    meubles.save()
    meubles.save()
    pourMaison.save()
    jardin.save()
    electro.save()

 
    sante = Category(categoryName='Santé et beauté')
    fournitures = Category(categoryName='Fournitures pour animaux')
    puericulture = Category(categoryName='Puériculture et enfants')
    jeux = Category(categoryName='Jouets et jeux')
    sante.save()
    fournitures.save()
    puericulture.save()
    jeux.save()

 
    femme = Category(categoryName='Vêtements et chaussures femmes')
    homme = Category(categoryName='Vêtements et chaussures hommes')
    bijoux = Category(categoryName='Bijoux et accessoires')
    sacs = Category(categoryName='Sacs et bagages')
    femme.save()
    homme.save()
    bijoux.save()
    sacs.save()

 
    velo = Category(categoryName = 'Vélo')
    creatif = Category(categoryName='Loisir créatifs')
    pieces = Category(categoryName='Piéces auto')
    sports = Category(categoryName='Sports et activités d\'extérieures')
    jeuxVideo = Category(categoryName='Jeux vidéo')
    livres = Category(categoryName='Livres,films et musique')
    instruments = Category(categoryName='Instruments de musique')
    antiquite = Category(categoryName='Antiquité et objets de collection')
    creatif.save()
    pieces.save()
    sports.save()
    jeuxVideo.save()
    livres.save()
    instruments.save()
    antiquite.save()
    velo.save()

  
    ordi=Category(categoryName='Electronique et ordinateurs')
    tele=Category(categoryName='Téléphones mobiles')
    ordi.save()
    tele.save()



    #Users
    u1 = User(email='test1@gmail.com',lastname = 'Lin',firstname ='Chih Huai',campus = woluwe, password='123', moderator=True)
    u2 = User(email='test2@gmail.com',lastname = 'Ali',firstname ='Abdulhamid',campus = woluwe, password='123', moderator=False)
    u1.save()   
    u2.save()
    ad1 = Ad(status = Ad.Status.TOSELL, title ='ad1', description= 'this is ad1',price = 69,category=outils, seller = u1)
    ad2 = Ad(status = Ad.Status.TOSELL, title ='ad2', description= 'this is ad2',price = 69,category=velo, seller = u1)
    ad3 = Ad(status = Ad.Status.TOSELL, title ='ad3', description= 'this is ad3',price = 69,category=sacs, seller = u2)
    ad4 = Ad(status = Ad.Status.TOSELL, title ='ad4', description= 'this is ad4',price = 69,category=jeuxVideo, seller = u2)
    ad1.save() 
    ad2.save()
    ad3.save()
    ad4.save()
    adcampLoc1 = AdsCampusLocation(ad=ad1,campus=louvain,location=UE4)
    adcampLoc2 = AdsCampusLocation(ad=ad1,campus=woluwe,location=WA249)
    adcampLoc3 = AdsCampusLocation(ad=ad2,campus=louvain,location=LO1)
    adcampLoc4 = AdsCampusLocation(ad=ad3,campus=Ixelles,location=AR)
    adcampLoc5 = AdsCampusLocation(ad=ad4,campus=louvain,location=CH41)
    adcampLoc6 = AdsCampusLocation(ad=ad4,campus=woluwe,location=CA1)
    adcampLoc7 = AdsCampusLocation(ad=ad4,campus=Ixelles,location=ARC59)
    adcampLoc1.save()
    adcampLoc2.save()
    adcampLoc3.save()
    adcampLoc4.save()
    adcampLoc5.save()
    adcampLoc6.save()
    adcampLoc7.save()
    
    me1 = Media(url='https://unsplash.com/photos/-wZtepNJlHg',ad=ad1)
    me2 = Media(url='https://imgflip.com/i/5wzqrj',ad=ad1)
    me3 = Media(url='https://unsplash.com/photos/pEHkamqczMU',ad=ad2)
    me4 = Media(url='https://unsplash.com/photos/JXECZL83E6M',ad=ad3)
    me5 = Media(url='https://unsplash.com/photos/YRmtGNQGMb8',ad=ad4)
    me1.save()
    me2.save()
    me3.save()
    me4.save()
    me5.save()


    return HttpResponse('Some stuff got added in the db')