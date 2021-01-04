from orm_db import *
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
@app.route('/pasif_listesi', methods=['GET', 'POST'])
@app.route('/pasif_listesi')
def pasif_listesi():
    try:
        ilanlar = Ilan.query.filter_by(isyeri_id=session['isyeri'],ilan_durum=1).all()
        return render_template('pasif_listesi.html',isveren=kullanici['isyeri'],ilanlar=ilanlar)
    except:
        return render_template('index.html', mesaj="Hoş Geldiniz")


#işveren pasif ilanlar sayfası işlemleri
@app.route('/basvurulan_listesi', methods=['GET', 'POST'])
@app.route('/basvurulan_listesi')
def basvurulan_listesi():
    ilanlar =Ilan.query.filter(Ilan.isyeri_id==session['isyeri'] and Ilan.ilan_durum == 0 and not (Ilan.basvuran_idler== None or Ilan.basvuran_idler=="")).all()
    try:
        return render_template('basvurulan_listesi.html',isveren=kullanici['isyeri'],ilanlar=ilanlar)
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




