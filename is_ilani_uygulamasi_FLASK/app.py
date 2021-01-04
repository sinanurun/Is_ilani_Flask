from orm_db import *
kullanici = {}

def uzanti_kontrol(dosyaadi):
   return '.' in dosyaadi and \
   dosyaadi.rsplit('.', 1)[1].lower() in UZANTILAR


# Giriş işlemlerinin yer alacak olduğu işlemler
#giriş karşılama sayfası
@app.route('/', methods=['GET', 'POST'])
@app.route('/')
def index():
    try:
        if request.method == 'POST':
            tc = request.form.get('tcno')
            sifre = request.form.get('sifre')
            k_tipi = int(request.form.get('kullanici'))
            if k_tipi == 0:
                user = Yonetici.query.filter_by(yonetici_tc=tc,yonetici_sifre=sifre).first()
                if user.yonetici_durum == 0:
                    session['yonetici'] = user.yonetici_id
                    kullanici['yonetici'] = user
                    return redirect(url_for('yonetici_sayfasi'))
                else:
                    return render_template('index.html', mesaj="Giriş Yapmak İstediğiniz Kullanıcı Aktif Değil")
            elif k_tipi == 1 :
                user = Isyeri.query.filter_by(isyeri_tc=tc, isyeri_sifre=sifre).first()
                if user.isyeri_durum == 0:
                    session['isyeri'] = user.isyeri_id
                    kullanici['isyeri'] = user

                    return redirect(url_for('isveren_sayfasi'))
                else:
                    return render_template('index.html', mesaj="Giriş Yapmak İstediğiniz Kullanıcı Aktif Değil")

            elif k_tipi == 2:
                user = Isci.query.filter_by(isci_tc=tc, isci_sifre=sifre).first()
                if user.isci_durum == 0:
                    session['isci'] = user.isci_id
                    kullanici['isci'] = user
                    return redirect(url_for('isci_sayfasi'))
                else:
                    return render_template('index.html', mesaj="Giriş Yapmak İstediğiniz Kullanıcı Aktif Değil")

            else:
                return render_template('index.html', mesaj="Giriş Yapmak İstediğiniz Kullanıcı Aktif Değil")
        else:
            return render_template('index.html', mesaj="Hoş Geldiniz")
    except:
        return render_template('index.html', mesaj="Hatalı Giriş Denemesi")

#çıkış işlemleri sayfası
@app.route('/cikis')
def cikis():
    session.clear()
    kullanici.clear()

    return redirect(url_for('index'))

#Aşağıdaki ilk bölümde yöneticilerin yapabilecek olduğu iş ve işlemlerin sayfa erişimleri yer almaktadır

#yönetici sayfası işlemleri
@app.route('/yonetici_sayfasi', methods=['GET', 'POST'])
@app.route('/yonetici_sayfasi')
def yonetici_sayfasi():
    try:
        ilanlar = Ilan.query.all()
        for ilan in ilanlar:
            ilan.ilan_tarihi = datetime.date(ilan.ilan_tarihi)


        # return redirect(url_for('ilan_listesi'))
        # return render_template('ilan_listesi.html',yonetici=kullanici['yonetici'])
        return render_template("yonetici.html",yonetici=kullanici['yonetici'],ilanlar=ilanlar)
    except:
        return render_template('index.html', mesaj="Hoş Geldiniz")


# İşçiler ile ilgili iş ve işlemleri aşağıdaki bölümde ifade edilmektedir.

# işçi ekleme işlemleri
@app.route('/isci_ekle', methods=['GET', 'POST'])
@app.route('/isci_ekle')
def isci_ekle():
    try:
        if request.method == 'POST':
            try:
                bilgiler = request.form.to_dict()
                tarih = datetime.strptime(bilgiler['isci_dogum_tarihi'], '%Y-%m-%d')
                tarih = datetime.date(tarih)

                dosya = request.files['isci_foto']
                if dosya and uzanti_kontrol(dosya.filename):
                    dosyaadi = bilgiler['isci_tc']+ secure_filename(dosya.filename)
                    dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
                    bilgiler['isci_foto'] = "/"+ app.config['UPLOAD_FOLDER'] + "/"+ dosyaadi
                    # return redirect(url_for('dosyayukleme',dosya=dosyaadi))
                else:
                    print("resim yüklenemedi")

                dosya = request.files['isci_ozgecmis']
                if dosya and uzanti_kontrol(dosya.filename):
                    dosyaadi = bilgiler['isci_tc']+secure_filename(dosya.filename)
                    dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
                    bilgiler['isci_ozgecmis'] = "/"+ app.config['UPLOAD_FOLDER'] +"/"+  dosyaadi
                    # return redirect(url_for('dosyayukleme',dosya=dosyaadi))
                else:
                    print("özgeçmiş yüklenemedi")

                multiselect = request.form.getlist('isci_meslek_idler')  # [temizlik,giyim,eğitim]
                bilgiler['isci_meslek_idler'] = str(multiselect)

                yeni_isci = Isci(isci_adi_soyadi=bilgiler['isci_adi_soyadi'], isci_tc=bilgiler['isci_tc'],
                                 isci_sifre=bilgiler['isci_sifre'],isci_cinsiyet=bilgiler['isci_cinsiyet'],
                                 isci_dogum_tarihi=tarih, isci_mezuniyet=int(bilgiler['isci_mezuniyet']),
                                 isci_askerlik=int(bilgiler['isci_askerlik']), isci_email=bilgiler['isci_email'],
                                 isci_tel=bilgiler['isci_tel'], isci_adres=bilgiler['isci_adres'],
                                 isci_foto=bilgiler['isci_foto'],isci_ozgecmis=bilgiler['isci_ozgecmis'],
                                 isci_meslek_idler=bilgiler['isci_meslek_idler'],
                                 isci_durum=int(bilgiler['isci_durum']), yonetici_id=session['yonetici'])
                dbsession.add(yeni_isci)
                dbsession.commit()
                return render_template("isci_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarı")
            except:
                return render_template("isci_ekle.html", yonetici=kullanici['yonetici'] , mesaj="Başarısızlık")
        else:
            mezuniyet = Mezun.query.all()
            askerlik = Askerlik.query.all()
            meslekler = Meslek.query.all()
            bilgiler = [mezuniyet, askerlik,meslekler]
            return render_template("isci_ekle.html", yonetici=kullanici['yonetici'], bilgiler=bilgiler)
    except:
        return render_template("isci_ekle.html", yonetici=kullanici['yonetici'])

 # isci güncelleme ve silme işlemleri
@app.route('/isci_guncelle_sil/<int:id>')
@app.route('/isci_guncelle_sil')
def isci_guncelle_sil(id=0):
    if id == 0:
        isciler = Isci.query.filter_by(yonetici_id=session['yonetici']).all()
        return render_template("isci_guncelle_sil.html", yonetici=kullanici['yonetici'], isciler=isciler)
    else:
        isciler = Isci.query.filter_by(isci_id=id).first()
        return redirect(url_for('isci_guncelle_sil'))


@app.route('/isci_guncelle/<int:id>')
@app.route('/isci_guncelle', methods=['GET', 'POST'])
def isci_guncelle(id=0):
    if id != 0:
        mezuniyet = Mezun.query.all()
        askerlik = Askerlik.query.all()
        meslek = Meslek.query.all()
        bilgiler = [mezuniyet, askerlik, meslek]
        isci = Isci.query.filter_by(isci_id=id).first()
        # tarih = datetime.strptime(, '%Y-%m-%d')
        tarih = datetime.date(isci.isci_dogum_tarihi)
        isci.isci_dogum_tarihi = tarih
        isci.isci_meslek_idler = eval(isci.isci_meslek_idler)
        return render_template("isci_guncelle.html", yonetici=kullanici['yonetici'], isciler=isci, bilgiler=bilgiler)
    elif request.method == 'POST':
        bilgiler = request.form.to_dict()
        tarih = datetime.strptime(bilgiler['isci_dogum_tarihi'], '%Y-%m-%d')
        tarih = datetime.date(tarih)
        bilgiler['isci_dogum_tarihi']=tarih
        dosya = request.files['isci_foto']
        if dosya and uzanti_kontrol(dosya.filename):
            dosyaadi = bilgiler['isci_tc'] + secure_filename(dosya.filename)
            dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
            bilgiler['isci_foto'] = "/" + app.config['UPLOAD_FOLDER'] + "/" + dosyaadi
            # return redirect(url_for('dosyayukleme',dosya=dosyaadi))
        else:
            print("resim yüklenemedi")

        dosya = request.files['isci_ozgecmis']
        if dosya and uzanti_kontrol(dosya.filename):
            dosyaadi = bilgiler['isci_tc'] + secure_filename(dosya.filename)
            dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
            bilgiler['isci_ozgecmis'] = "/" + app.config['UPLOAD_FOLDER'] + "/" + dosyaadi
            # return redirect(url_for('dosyayukleme',dosya=dosyaadi))
        else:
            print("özgeçmiş yüklenemedi")

        multiselect = request.form.getlist('isci_meslek_idler')  # [temizlik,giyim,eğitim]
        bilgiler['isci_meslek_idler'] = str(multiselect)
        dbsession.query(Isci).filter(Isci.isci_id==bilgiler['isci_id']).update(bilgiler)
        dbsession.commit()
        return redirect(url_for('isci_guncelle_sil'))
    else:
        return redirect(url_for('isci_guncelle'))

#işçi silme işlemi yapmak için aşağıdaki kod bloğu
@app.route('/isci_sil/<int:sil>')
def isci_sil(sil=0):
    if sil != 0:
        dbsession.query(Isci).filter(Isci.isci_id == sil).delete()
        dbsession.commit()
        return redirect(url_for('isci_guncelle_sil'))
    else:
        return redirect(url_for('isci_guncelle_sil'))

# İşveren ile ilgili iş ve işlemleri aşağıdaki bölümde ifade edilmektedir.

# işveren ekleme işlemleri
@app.route('/isveren_ekle', methods=['GET', 'POST'])
@app.route('/isveren_ekle')
def isveren_ekle():
    try:
        if request.method == 'POST':
            try:
                bilgiler = request.form.to_dict()
                dosya = request.files['isyeri_foto']
                if dosya and uzanti_kontrol(dosya.filename):
                    dosyaadi = bilgiler['isyeri_tc'] + secure_filename(dosya.filename)
                    dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
                    bilgiler['isyeri_foto'] = "/" + app.config['UPLOAD_FOLDER'] + "/" + dosyaadi
                    # return redirect(url_for('dosyayukleme',dosya=dosyaadi))
                else:
                    print("resim yüklenemedi")
                yeni_isyeri = Isyeri(isyeri_adi=bilgiler['isyeri_adi'], isyeri_yonetici_adi_soyadi=bilgiler['isyeri_yonetici_adi_soyadi'],
                                     isyeri_tc=bilgiler['isyeri_tc'], isyeri_sifre=bilgiler['isyeri_sifre'],
                                     isyeri_email=bilgiler['isyeri_email'], isyeri_tel=bilgiler['isyeri_tel'],
                                     isyeri_adres=bilgiler['isyeri_adres'], isyeri_durum=int(bilgiler['isyeri_durum']),
                                     isyeri_foto=bilgiler['isyeri_foto'], yonetici_id=session['yonetici'])
                dbsession.add(yeni_isyeri)
                dbsession.commit()

                return render_template("isveren_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarı")
            except:
                return render_template("isveren_ekle.html", yonetici=kullanici['yonetici'] , mesaj="Başarısızlık")
        else:
            return render_template("isveren_ekle.html", yonetici=kullanici['yonetici'])

    except:
        return render_template("isveren_ekle.html", yonetici=kullanici['yonetici'])

#  # isveren güncelleme ve silme işlemleri
@app.route('/isveren_guncelle_sil/<int:id>')
@app.route('/isveren_guncelle_sil')
def isveren_guncelle_sil(id=0):
    if id == 0:
        isverenler = Isyeri.query.filter_by(yonetici_id=session['yonetici']).all()
        return render_template("isveren_guncelle_sil.html", yonetici=kullanici['yonetici'], isverenler=isverenler)
    else:
        isverenler= Isyeri.query.filter_by(isyeri_id=id).first()
        return redirect(url_for('isyeri_guncelle_sil'))

@app.route('/isveren_guncelle/<int:id>')
@app.route('/isveren_guncelle', methods=['GET', 'POST'])
def isveren_guncelle(id=0):
    try:
        if id != 0:
            isveren = Isyeri.query.filter_by(isyeri_id=id).first()
            return render_template("isveren_guncelle.html", yonetici=kullanici['yonetici'], isveren=isveren)
        elif request.method == 'POST':
            bilgiler = request.form.to_dict()

            dosya = request.files['isyeri_foto']
            if dosya and uzanti_kontrol(dosya.filename):
                dosyaadi = bilgiler['isyeri_tc'] + secure_filename(dosya.filename)
                dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
                bilgiler['isyeri_foto'] = "/" + app.config['UPLOAD_FOLDER'] + "/" + dosyaadi
                # return redirect(url_for('dosyayukleme',dosya=dosyaadi))
            else:
                print("resim yüklenemedi")

            dbsession.query(Isyeri).filter(Isyeri.isyeri_id==bilgiler['isyeri_id']).update(bilgiler)
            dbsession.commit()
            return redirect(url_for('isveren_guncelle_sil'))
        else:
            return redirect(url_for('isveren_guncelle'))
    except:
        return redirect(url_for('isveren_guncelle_sil'))
#
#işveren silme işlemi yapmak için aşağıdaki kod bloğu
@app.route('/isveren_sil/<int:sil>')
def isveren_sil(sil=0):
    if sil != 0:
        dbsession.query(Isyeri).filter(Isyeri.isyeri_id == sil).delete()
        dbsession.commit()
        return redirect(url_for('isveren_guncelle_sil'))
    else:
        return redirect(url_for('isveren_guncelle_sil'))

# yönetici ilan işlemleri

#ilan ekleme işlemleri
@app.route('/ilan_ekle', methods=['GET', 'POST'])
@app.route('/ilan_ekle')
def ilan_ekle():
    try:
        if request.method == 'POST':
            try:
                bilgiler = request.form.to_dict()
                tarih = datetime.strptime(bilgiler['ilan_tarihi'], '%Y-%m-%d')
                tarih = datetime.date(tarih)

                multiselect = request.form.getlist('meslek_idler')  # [temizlik,giyim,eğitim]
                bilgiler['meslek_idler'] = str(multiselect)
                # bilgiler['anahtar_kelimeler'] = str(bilgiler['anahtar_kelimeler'].split(","))


                yeni_ilan = Ilan(yonetici_id=session['yonetici'], ilan_baslik=bilgiler['ilan_baslik'],
                                 ilan_icerik=bilgiler['ilan_icerik'], isyeri_id=int(bilgiler['isyeri_id']),
                                 ilan_durum=int(bilgiler['ilan_durum']),
                                 ilan_tarihi=tarih, meslek_idler=bilgiler['meslek_idler'],
                                 anahtarkelime_idler=bilgiler['anahtar_kelimeler'])
                dbsession.add(yeni_ilan)
                dbsession.commit()
                return render_template("ilan_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarı")

            except:
                return render_template("ilan_ekle.html", yonetici=kullanici['yonetici'], mesaj="Başarısızlık")
        else:
            meslekler = Meslek.query.all()
            isyeri = Isyeri.query.filter_by(isyeri_durum=0).all()
            return render_template("ilan_ekle.html", yonetici=kullanici['yonetici'], isyeri=isyeri,meslekler=meslekler)

    except:
        isyeri = Isyeri.query.filter_by(isyeri_durum=0).all()
        return render_template("ilan_ekle.html", yonetici=kullanici['yonetici'], isyeri=isyeri)


#ilan listeleme işlemleri
@app.route('/ilan_listesi', methods=['GET', 'POST'])
@app.route('/ilan_listesi')
def ilan_listesi():
    try:
        ilanlar = Ilan.query.all()
        return render_template("ilan_listesi.html", yonetici=kullanici['yonetici'], ilanlar=ilanlar)
    except:
        return render_template("ilan_listesi.html", yonetici=kullanici['yonetici'])

# ilan güncelleme ve silme işlemleri
@app.route('/ilan_guncelle_sil/<int:id>')
@app.route('/ilan_guncelle_sil')
def ilan_guncelle_sil(id=0):
    if id == 0:
        ilanlar = Ilan.query.all()
        meslekler = Meslek.query.all()
        return render_template("ilan_guncelle_sil.html", yonetici=kullanici['yonetici'], ilanlar=ilanlar,meslekler=meslekler)
    else:
        return redirect(url_for('ilan_guncelle_sil'))

@app.route('/ilan_sil/<int:sil>')
def ilan_sil(sil=0):
    if sil != 0:
        dbsession.query(Ilan).filter(Ilan.ilan_id== sil).delete()
        dbsession.commit()
        return redirect(url_for('ilan_guncelle_sil'))

@app.route('/ilan_guncelle/<int:id>')
@app.route('/ilan_guncelle', methods=['GET', 'POST'])
def ilan_guncelle(id=0):
    if id != 0:
        ilan = Ilan.query.filter_by(ilan_id=id).first()
        tarih = datetime.date(ilan.ilan_tarihi)
        ilan.ilan_tarihi=tarih
        isyeri = Isyeri.query.all()
        meslekler = Meslek.query.all()
        return render_template("ilan_guncelle.html", yonetici=kullanici['yonetici'], ilan=ilan,isyeri=isyeri,meslekler=meslekler)
    elif request.method == 'POST':
        bilgiler = request.form.to_dict()
        tarih = datetime.strptime(bilgiler['ilan_tarihi'], '%Y-%m-%d')
        tarih = datetime.date(tarih)
        bilgiler['ilan_tarihi'] = tarih
        multiselect = request.form.getlist('meslek_idler')  # [temizlik,giyim,eğitim]
        bilgiler['meslek_idler'] = str(multiselect)
        dbsession.query(Ilan).filter(Ilan.ilan_id == bilgiler['ilan_id']).update(bilgiler)
        dbsession.commit()
        return redirect(url_for('ilan_guncelle_sil'))
    else:
        return redirect(url_for('ilan_guncelle'))


#
# işveren işlemleri aşağıdaki kod bloğunda yapılacaktır
#

#işveren sayfası işlemleri
@app.route('/isveren_sayfasi', methods=['GET', 'POST'])
@app.route('/isveren_sayfasi')
def isveren_sayfasi():
    try:
        ilanlar = Ilan.query.filter_by(isyeri_id=session['isyeri'],ilan_durum=0).all()
        return render_template('isveren.html',isveren=kullanici['isyeri'],ilanlar=ilanlar)
    except:
        return render_template('index.html', mesaj="Hoş Geldiniz")

# işveren ilan detayı
@app.route('/isveren_ilan_detay/<int:id>')
@app.route('/isveren_ilan_detay', methods=['GET', 'POST'])
def isveren_ilan_detay(id=0):
    if id != 0:
        ilan = Ilan.query.filter_by(ilan_id=id).first()
        tarih = datetime.date(ilan.ilan_tarihi)
        ilan.ilan_tarihi=tarih
        basvuranlar = str(ilan.basvuran_idler).split(",")
        kisiler = []
        for kisi in basvuranlar:
            if kisi != "":
                kisiler.append(Isci.query.filter_by(isci_id=int(kisi)).first())
        return render_template("isveren_ilan_detay.html", isveren=kullanici['isyeri'], ilan=ilan, isciler=kisiler)
    else:
        return redirect(url_for('isveren_sayfasi'))


#işveren pasif ilanlar sayfası işlemleri
@app.route('/isveren_pasif_listesi', methods=['GET', 'POST'])
@app.route('/isveren_pasif_listesi')
def isveren_pasif_listesi():
    try:
        ilanlar = Ilan.query.filter_by(isyeri_id=session['isyeri'],ilan_durum=1).all()
        return render_template('isveren_pasif_listesi.html',isveren=kullanici['isyeri'],ilanlar=ilanlar)
    except:
        return render_template('index.html', mesaj="Hoş Geldiniz")


#işveren pasif ilanlar sayfası işlemleri
@app.route('/isveren_basvurulan_listesi', methods=['GET', 'POST'])
@app.route('/isveren_basvurulan_listesi')
def isveren_basvurulan_listesi():
    ilanlar =Ilan.query.filter(Ilan.isyeri_id==session['isyeri'] and Ilan.ilan_durum == 0 and not (Ilan.basvuran_idler== None or Ilan.basvuran_idler=="")).all()
    try:
        return render_template('isveren_basvurulan_listesi.html',isveren=kullanici['isyeri'],ilanlar=ilanlar)
    except:
        return render_template('index.html', mesaj="Hoş Geldiniz")

# işveren ilan detayı
@app.route('/isveren_basvuran_detay/<int:id>/<int:iid>')
def isveren_basvuran_detay(id=0,iid=0):
    if id != 0:
        ilan = Ilan.query.filter_by(ilan_id=id).first()
        tarih = datetime.date(ilan.ilan_tarihi)
        ilan.ilan_tarihi=tarih
        isci = Isci.query.filter_by(isci_id=iid).first()
        meslekler = Meslek.query.all()
        return render_template("isveren_basvuran_detay.html", isveren=kullanici['isyeri'], isci=isci,meslekler=meslekler)
    else:
        return redirect(url_for('isveren_sayfasi'))



#
# işçi işlemleri aşağıdaki kod bloğunda yapılacaktır
#işçi sayfası işlemleri
@app.route('/isci_sayfasi', methods=['GET', 'POST'])
@app.route('/isci_sayfasi')
def isci_sayfasi():

    meslekler = Meslek.query.all()
    ilanlar = Ilan.query.filter_by(ilan_durum=0).all()
    bilanlar = [] #başvurulabilir
    pilanlar = [] #başvurulamaz
    isci_meslekleri = eval(kullanici['isci'].isci_meslek_idler)
    for ilan in ilanlar:
        try:
            basvuranlar = str(ilan.basvuran_idler).split(",")
            for meslek in meslekler:
                if (meslek.meslek_id.__str__() in isci_meslekleri) and not(str(session['isci']) in basvuranlar):
                    bilanlar.append(ilan)
                    break
                elif (meslek.meslek_id.__str__() in isci_meslekleri) and (str(session['isci']) in basvuranlar):
                    pilanlar.append(ilan)
                    break
        except:
            if ilan.basvuran_idler == "":
                for meslek in meslekler:
                    if meslek.meslek_id.__str__() in isci_meslekleri:
                        bilanlar.append(ilan)
                        break
    return render_template('isci.html',isci=kullanici['isci'], ilanlar=bilanlar, pilanlar=pilanlar)


# işveren ilan detayı
@app.route('/isci_ilan_detay/<int:id>/<int:iid>')
@app.route('/isci_ilan_detay/<int:id>')
@app.route('/isci_ilan_detay', methods=['GET', 'POST'])
def isci_ilan_detay(id=0,iid=0):
    if id != 0 and iid ==0 :
        ilan = Ilan.query.filter_by(ilan_id=id).first()
        tarih = datetime.date(ilan.ilan_tarihi)
        ilan.ilan_tarihi = tarih
        basvuranlar = str(ilan.basvuran_idler).split(",")
        if str(session['isci']) in basvuranlar:
            basvuru = True
        else:
            basvuru = False
        meslekler = Meslek.query.all()

        return render_template("isci_ilan_detay.html", isci=kullanici['isci'],
                               ilan=ilan,basvuru=basvuru,meslekler=meslekler)
    elif id !=0 and iid !=0:
        ilan = Ilan.query.filter_by(ilan_id=id).first()
        idler = ilan.basvuran_idler + ","+ str(iid)
        dbsession.query(Ilan).filter(Ilan.ilan_id ==id).update({Ilan.basvuran_idler:idler})
        dbsession.commit()
        return redirect(url_for('isci_basvurulan_listesi'))
    else:
        return redirect(url_for('isci_sayfasi'))
#
#
#işveren pasif ilanlar sayfası işlemleri
@app.route('/isci_pasif_listesi', methods=['GET', 'POST'])
@app.route('/isci_pasif_listesi')
def isci_pasif_listesi():
    try:
        ilanlar = Ilan.query.filter_by(ilan_durum=1).all()
        pilanlar = []
        for ilan in ilanlar:
            try:
                basvuranlar = str(ilan.basvuran_idler).split(",")
                if str(session['isci']) in basvuranlar:
                    pilanlar.append(ilan)
            except:
                pass
        return render_template('isci_pasif_listesi.html',isci=kullanici['isci'],ilanlar=pilanlar)
    except:
        return render_template('index.html', mesaj="Hoş Geldiniz")


#işçi başvurulan ilanlar sayfası işlemleri
@app.route('/isci_basvurulan_listesi', methods=['GET', 'POST'])
@app.route('/isci_basvurulan_listesi')
def isci_basvurulan_listesi():
    try:
        ilanlar = Ilan.query.filter_by(ilan_durum=0).all()
        pilanlar = []
        for ilan in ilanlar:
            try:
                basvuranlar = str(ilan.basvuran_idler).split(",")
                if str(session['isci']) in basvuranlar:
                    pilanlar.append(ilan)
            except:
                pass
        return render_template('isci_basvurulan_listesi.html',isci=kullanici['isci'],ilanlar=pilanlar)
    except:
        return render_template('index.html', mesaj="Hoş Geldiniz")
#
@app.route('/isveren_bilgi_guncelle')
@app.route('/isveren_bilgi_guncelle', methods=['GET', 'POST'])
def isveren_bilgi_guncelle(id=0):
    try:
        if request.method == 'POST':
            bilgiler = request.form.to_dict()
            dosya = request.files['isyeri_foto']
            if dosya and uzanti_kontrol(dosya.filename):
                dosyaadi = bilgiler['isyeri_tc'] + secure_filename(dosya.filename)
                dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
                bilgiler['isyeri_foto'] = "/" + app.config['UPLOAD_FOLDER'] + "/" + dosyaadi
                # return redirect(url_for('dosyayukleme',dosya=dosyaadi))
            dbsession.query(Isyeri).filter(Isyeri.isyeri_id==bilgiler['isyeri_id']).update(bilgiler)
            dbsession.commit()
            return render_template("isveren_bilgi_guncelle.html", mesaj="Güncelleme Başarılı")
        elif session['isyeri']:
            isveren = Isyeri.query.filter_by(isyeri_id=session['isyeri']).first()
            return render_template("isveren_bilgi_guncelle.html", isveren=isveren)
        else:
            return render_template("isveren_bilgi_guncelle.html", mesaj="Güncelleme Başarısız")
    except:
        return redirect(url_for('isveren_bilgi_guncelle'))



#isveren ilan ekleme işlemleri
@app.route('/isveren_ilan_ekle', methods=['GET', 'POST'])
@app.route('/isveren_ilan_ekle')
def isveren_ilan_ekle():
    try:
        if request.method == 'POST':
            try:
                bilgiler = request.form.to_dict()
                tarih = datetime.strptime(bilgiler['ilan_tarihi'], '%Y-%m-%d')
                tarih = datetime.date(tarih)

                multiselect = request.form.getlist('meslek_idler')  # [temizlik,giyim,eğitim]
                bilgiler['meslek_idler'] = str(multiselect)
                # bilgiler['anahtar_kelimeler'] = str(bilgiler['anahtar_kelimeler'].split(","))


                yeni_ilan = Ilan(yonetici_id=kullanici['isyeri'].yonetici_id, ilan_baslik=bilgiler['ilan_baslik'],
                                 ilan_icerik=bilgiler['ilan_icerik'], isyeri_id=session['isyeri'],
                                 ilan_durum=int(bilgiler['ilan_durum']),
                                 ilan_tarihi=tarih, meslek_idler=bilgiler['meslek_idler'],
                                 anahtarkelime_idler=bilgiler['anahtar_kelimeler'])
                dbsession.add(yeni_ilan)
                dbsession.commit()
                return render_template("isveren_ilan_ekle.html", isveren=kullanici['isyeri'], mesaj="Başarı")

            except:
                return render_template("isveren_ilan_ekle.html", isveren=kullanici['isyeri'], mesaj="Başarısızlık")
        else:
            meslekler = Meslek.query.all()
            isyeri = Isyeri.query.filter_by(isyeri_id=session['isyeri']).first()
            return render_template("isveren_ilan_ekle.html", isveren=isyeri,meslekler=meslekler)

    except:
        isyeri = Isyeri.query.filter_by(isyeri_durum=0).all()
        return render_template("isveren_ilan_ekle.html",  isveren=isyeri)

# # işveren ilan detayı
# @app.route('/isveren_basvuran_detay/<int:id>/<int:iid>')
# def isveren_basvuran_detay(id=0,iid=0):
#     if id != 0:
#         ilan = Ilan.query.filter_by(ilan_id=id).first()
#         tarih = datetime.date(ilan.ilan_tarihi)
#         ilan.ilan_tarihi=tarih
#         isci = Isci.query.filter_by(isci_id=iid).first()
#
#         basvuranlar = str(ilan.basvuran_idler).split(",")
#         kisiler = []
#         for kisi in basvuranlar:
#             kisiler.append(Isci.query.filter_by(isci_id=int(kisi)).first())
#
#         return render_template("isveren_basvuran_detay.html", isveren=kullanici['isyeri'], ilan=ilan,isci=isci,isciler=kisiler)
#     else:
#         return redirect(url_for('isveren_sayfasi'))


# ilan güncelleme ve silme işlemleri
@app.route('/isveren_ilan_guncelle_sil/<int:id>')
@app.route('/isveren_ilan_guncelle_sil')
def isveren_ilan_guncelle_sil(id=0):
    if id == 0:
        ilanlar = Ilan.query.filter_by(isyeri_id=session['isyeri']).all()
        meslekler = Meslek.query.all()
        return render_template("isveren_ilan_guncelle_sil.html", isveren=kullanici['isyeri'], ilanlar=ilanlar,meslekler=meslekler)
    else:
        return redirect(url_for('isveren_ilan_guncelle_sil'))

@app.route('/isveren_ilan_sil/<int:sil>')
def isveren_ilan_sil(sil=0):
    if sil != 0:
        dbsession.query(Ilan).filter(Ilan.ilan_id== sil).delete()
        dbsession.commit()
        return redirect(url_for('isveren_ilan_guncelle_sil'))

@app.route('/isveren_ilan_guncelle/<int:id>')
@app.route('/isveren_ilan_guncelle', methods=['GET', 'POST'])
def isveren_ilan_guncelle(id=0):
    if id != 0:
        ilan = Ilan.query.filter_by(ilan_id=id).first()
        tarih = datetime.date(ilan.ilan_tarihi)
        ilan.ilan_tarihi=tarih
        meslekler = Meslek.query.all()
        return render_template("isveren_ilan_guncelle.html", isveren=kullanici['isyeri'], ilan=ilan,meslekler=meslekler)
    elif request.method == 'POST':
        bilgiler = request.form.to_dict()
        tarih = datetime.strptime(bilgiler['ilan_tarihi'], '%Y-%m-%d')
        tarih = datetime.date(tarih)
        bilgiler['ilan_tarihi'] = tarih
        multiselect = request.form.getlist('meslek_idler')  # [temizlik,giyim,eğitim]
        bilgiler['meslek_idler'] = str(multiselect)
        dbsession.query(Ilan).filter(Ilan.ilan_id == bilgiler['ilan_id']).update(bilgiler)
        dbsession.commit()
        return redirect(url_for('isveren_ilan_guncelle_sil'))
    else:
        return redirect(url_for('isveren_ilan_guncelle'))

@app.route('/isci_bilgi_guncelle', methods=['GET', 'POST'])
def isci_bilgi_guncelle(id=0):
    if request.method == 'POST':
        bilgiler = request.form.to_dict()
        tarih = datetime.strptime(bilgiler['isci_dogum_tarihi'], '%Y-%m-%d')
        tarih = datetime.date(tarih)
        bilgiler['isci_dogum_tarihi']=tarih
        dosya = request.files['isci_foto']
        if dosya and uzanti_kontrol(dosya.filename):
            dosyaadi = bilgiler['isci_tc'] + secure_filename(dosya.filename)
            dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
            bilgiler['isci_foto'] = "/" + app.config['UPLOAD_FOLDER'] + "/" + dosyaadi
            # return redirect(url_for('dosyayukleme',dosya=dosyaadi))
        else:
            print("resim yüklenemedi")

        dosya = request.files['isci_ozgecmis']

        if dosya and uzanti_kontrol(dosya.filename):
            dosyaadi = bilgiler['isci_tc'] + secure_filename(dosya.filename)
            dosya.save(os.path.join(app.config['UPLOAD_FOLDER'], dosyaadi))
            bilgiler['isci_ozgecmis'] = "/" + app.config['UPLOAD_FOLDER'] + "/" + dosyaadi
            # return redirect(url_for('dosyayukleme',dosya=dosyaadi))
        else:
            print("özgeçmiş yüklenemedi")

        multiselect = request.form.getlist('isci_meslek_idler')  # [temizlik,giyim,eğitim]
        bilgiler['isci_meslek_idler'] = str(multiselect)
        dbsession.query(Isci).filter(Isci.isci_id==bilgiler['isci_id']).update(bilgiler)
        dbsession.commit()
        return redirect(url_for('isci_bilgi_guncelle'))

    elif kullanici['isci']:
        mezuniyet = Mezun.query.all()
        askerlik = Askerlik.query.all()
        meslek = Meslek.query.all()
        bilgiler = [mezuniyet, askerlik, meslek]
        isci = Isci.query.filter_by(isci_id=session['isci']).first()
        # tarih = datetime.strptime(, '%Y-%m-%d')
        tarih = datetime.date(isci.isci_dogum_tarihi)
        isci.isci_dogum_tarihi = tarih
        isci.isci_meslek_idler = eval(isci.isci_meslek_idler)
        return render_template("isci_bilgi_guncelle.html", isci=kullanici['isci'], isciler=isci, bilgiler=bilgiler)



    else:
        return redirect(url_for('isci_bilgi_guncelle'))

@app.route('/isci_ilan_guncelle/<int:id>')
def isci_ilan_guncelle(id=0):
    if id != 0:
        ilan = Ilan.query.filter_by(ilan_id=id).first()
        basvuran_idler = ilan.basvuran_idler.replace(str(session['isci']),"")
        dbsession.query(Ilan).filter_by(ilan_id=id).update({Ilan.basvuran_idler : basvuran_idler})
        dbsession.commit()
        return redirect(url_for('isci_sayfasi'))
    else:
        return redirect(url_for('isci_sayfasi'))

# işveren ilan detayı
@app.route('/yonetici_ilan_detay/<int:id>')
@app.route('/yonetici_ilan_detay', methods=['GET', 'POST'])
def yonetici_ilan_detay(id=0):
    if id != 0:
        ilan = Ilan.query.filter_by(ilan_id=id).first()
        tarih = datetime.date(ilan.ilan_tarihi)
        ilan.ilan_tarihi=tarih
        basvuranlar = str(ilan.basvuran_idler).split(",")
        kisiler = []
        for kisi in basvuranlar:
            if kisi != "":
                kisiler.append(Isci.query.filter_by(isci_id=int(kisi)).first())
        return render_template("yonetici_ilan_detay.html", yonetici=kullanici['yonetici'], ilan=ilan, isciler=kisiler)
    else:
        return redirect(url_for('yonetici_sayfasi'))

# işveren ilan detayı
@app.route('/yonetici_basvuran_detay/<int:id>/<int:iid>')
def yonetici_basvuran_detay(id=0,iid=0):
    if id != 0:
        isci = Isci.query.filter_by(isci_id=iid).first()
        meslekler = Meslek.query.all()
        return render_template("yonetici_basvuran_detay.html", yonetici=kullanici['yonetici'], isci=isci,meslekler=meslekler)
    else:
        return redirect(url_for('yonetici_sayfasi'))

# işveren ilan detayı
@app.route('/yonetici_firma_detay/<int:id>/<int:iid>')
def yonetici_firma_detay(id=0,iid=0):
    if id != 0:
        isyeri = Isyeri.query.filter_by(isyeri_id=iid).first()
        return render_template("yonetici_firma_detay.html", yonetici=kullanici['yonetici'], isyeri=isyeri)
    else:
        return redirect(url_for('yonetici_sayfasi'))


if __name__ == '__main__':
    app.run(debug=True)
