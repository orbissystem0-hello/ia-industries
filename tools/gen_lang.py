# -*- coding: utf-8 -*-
"""Generates extra Minecraft lang files for ia_industries. Order: cargo_copter, cargo_gyrodyne, cargo_biplane, cargo_seaplane, gigantia, pelican, hawk, dragonfly."""
import json, os, sys
IDS = ['cargo_copter', 'cargo_gyrodyne', 'cargo_biplane', 'cargo_seaplane', 'gigantia', 'pelican', 'hawk', 'dragonfly']
GROUP = 'Create: Immersive Aircraft Industries'
L = {}
L['es_es'] = (['Cuadricóptero de carga', 'Girodino de carga', 'Biplano de carga', 'Hidroavión de carga', 'Gigantia', 'Pelícano', 'Halcón', 'Libélula'], [
 'Un transporte lento basado en el Quadrocopter. Odia el viento.',
 'Un girodino con bodega y motor. Consume combustible, despega en vertical y tarda en ganar velocidad hacia delante.',
 'Un biplano bimotor con cofres donde antes estaban los asientos.',
 'Un hidroavión que lleva sus cofres detrás de la cabina.',
 'Seis motores y alas interminables. Despega con facilidad, ignora el viento y es el que más carga.',
 'El más rápido sobre el agua, donde funcionan los cuatro motores. Solo despega si tiras con firmeza de la palanca y en el aire es lento y torpe.',
 'Una cañonera que ignora el viento. La ballesta ventral hace el doble de daño; los dos autocañones bajo las alas disparan y golpean 1,5 veces más fuerte.',
 'Dos rotores en brazos laterales y una cámara acorazada colgada del vientre. Consume combustible, despega en vertical y acelera despacio.'])
L['es_mx'] = L['es_es']
L['fr_fr'] = (['Quadrocoptère cargo', 'Gyrodyne cargo', 'Biplan cargo', 'Hydravion cargo', 'Gigantia', 'Pélican', 'Faucon', 'Libellule'], [
 'Un transporteur lent basé sur le Quadrocopter. Déteste le vent.',
 'Un gyrodyne avec soute et moteur. Consomme du carburant, décolle à la verticale et met du temps à prendre de la vitesse vers l’avant.',
 'Un biplan bimoteur avec des coffres à la place des sièges.',
 'Un hydravion qui transporte ses coffres derrière la cabine.',
 'Six moteurs et des ailes interminables. Décolle facilement, ignore le vent et transporte le plus.',
 'Le plus rapide sur l’eau, où ses quatre moteurs tournent. Il ne quitte l’eau que si vous tirez franchement sur le manche, et il est lent et maladroit en l’air.',
 'Un canonnier qui ignore le vent. La baliste ventrale inflige le double de dégâts ; les deux canons automatiques sous les ailes tirent et frappent 1,5 fois plus fort.',
 'Deux rotors sur des poutres latérales et un coffre-fort suspendu sous le ventre. Consomme du carburant, décolle à la verticale et accélère lentement.'])
L['de_de'] = (['Fracht-Quadrocopter', 'Fracht-Gyrodyne', 'Fracht-Doppeldecker', 'Fracht-Wasserflugzeug', 'Gigantia', 'Pelikan', 'Falke', 'Libelle'], [
 'Ein langsamer Lastenträger auf Basis des Quadrocopters. Hasst Wind.',
 'Ein Gyrodyne mit Laderaum und Motor. Verbraucht Treibstoff, startet senkrecht und braucht eine Weile, um nach vorn Fahrt aufzunehmen.',
 'Ein zweimotoriger Doppeldecker mit Truhen anstelle der Sitze.',
 'Ein Flugboot, das seine Truhen hinter der Kabine trägt.',
 'Sechs Motoren und endlose Flügel. Hebt leicht ab, ignoriert Wind und transportiert am meisten.',
 'Am schnellsten über dem Wasser, wo alle vier Motoren laufen. Es verlässt das Wasser nur, wenn man kräftig hochzieht, und ist in der Luft langsam und träge.',
 'Ein Kampfhubschrauber, der Wind ignoriert. Die Bauch-Ballista richtet doppelten Schaden an; die beiden Maschinenkanonen unter den Tragflächen feuern und treffen 1,5-mal so hart.',
 'Zwei Rotoren an seitlichen Auslegern und ein Tresor unter dem Bauch. Verbraucht Treibstoff, startet senkrecht und beschleunigt langsam.'])
L['ru_ru'] = (['Грузовой квадрокоптер', 'Грузовой гиродин', 'Грузовой биплан', 'Грузовой гидросамолёт', 'Гигантия', 'Пеликан', 'Ястреб', 'Стрекоза'], [
 'Медленный грузовик на основе квадрокоптера. Ненавидит ветер.',
 'Гиродин с грузовым отсеком и двигателем. Расходует топливо, взлетает вертикально и не сразу набирает скорость вперёд.',
 'Двухмоторный биплан с сундуками на месте сидений.',
 'Летающая лодка, которая возит сундуки за кабиной.',
 'Шесть двигателей и бесконечные крылья. Легко взлетает, игнорирует ветер и перевозит больше всех.',
 'Быстрее всех над водой, где работают все четыре двигателя. Отрывается от воды, только если уверенно потянуть штурвал на себя, а в воздухе медлителен и неповоротлив.',
 'Канонерка, которой не страшен ветер. Баллиста под брюхом наносит двойной урон; две автопушки под крыльями стреляют и бьют в 1,5 раза сильнее.',
 'Два винта на боковых балках и хранилище под брюхом. Расходует топливо, взлетает вертикально и медленно разгоняется.'])
L['pt_br'] = (['Quadricóptero de carga', 'Girodino de carga', 'Biplano de carga', 'Hidroavião de carga', 'Gigantia', 'Pelicano', 'Falcão', 'Libélula'], [
 'Um transportador lento baseado no Quadrocopter. Odeia vento.',
 'Um girodino com compartimento de carga e motor. Gasta combustível, decola na vertical e demora a ganhar velocidade para a frente.',
 'Um biplano bimotor com baús no lugar dos assentos.',
 'Um hidroavião que leva os baús atrás da cabine.',
 'Seis motores e asas sem fim. Decola com facilidade, ignora o vento e carrega mais que todos.',
 'O mais rápido sobre a água, onde os quatro motores funcionam. Só sai da água se você puxar com firmeza e, no ar, é lento e desajeitado.',
 'Uma canhoneira que ignora o vento. A balista na barriga causa o dobro de dano; os dois canhões automáticos sob as asas disparam e acertam 1,5 vez mais forte.',
 'Dois rotores em vigas laterais e um cofre pendurado na barriga. Gasta combustível, decola na vertical e acelera devagar.'])
L['pt_pt'] = L['pt_br']
L['it_it'] = (['Quadricottero da carico', 'Girodina da carico', 'Biplano da carico', 'Idrovolante da carico', 'Gigantia', 'Pellicano', 'Falco', 'Libellula'], [
 'Un lento trasportatore basato sul Quadrocopter. Odia il vento.',
 'Una girodina con vano di carico e motore. Consuma carburante, decolla in verticale e impiega un po’ ad acquistare velocità in avanti.',
 'Un biplano bimotore con bauli al posto dei sedili.',
 'Un idrovolante che porta i bauli dietro l’abitacolo.',
 'Sei motori e ali infinite. Decolla con facilità, ignora il vento e trasporta più di tutti.',
 'Il più veloce sull’acqua, dove funzionano tutti e quattro i motori. Lascia l’acqua solo se tiri con decisione la cloche ed è lento e goffo in aria.',
 'Una cannoniera che ignora il vento. La balista ventrale infligge danni doppi; i due cannoni automatici sotto le ali sparano e colpiscono 1,5 volte più forte.',
 'Due rotori su travi laterali e un caveau appeso sotto la pancia. Consuma carburante, decolla in verticale e accelera lentamente.'])
L['pl_pl'] = (['Kwadrokopter towarowy', 'Żyrodyn towarowy', 'Dwupłatowiec towarowy', 'Wodnosamolot towarowy', 'Gigantia', 'Pelikan', 'Jastrząb', 'Ważka'], [
 'Powolny transporter oparty na kwadrokopterze. Nienawidzi wiatru.',
 'Żyrodyn z ładownią i silnikiem. Spala paliwo, startuje pionowo i dość długo nabiera prędkości do przodu.',
 'Dwusilnikowy dwupłatowiec ze skrzyniami w miejscu foteli.',
 'Łódź latająca, która wozi skrzynie za kabiną.',
 'Sześć silników i skrzydła bez końca. Łatwo startuje, ignoruje wiatr i zabiera najwięcej.',
 'Najszybszy nad wodą, gdzie pracują wszystkie cztery silniki. Odrywa się od wody tylko po mocnym pociągnięciu drążka, a w powietrzu jest wolny i niezgrabny.',
 'Kanonierka, której wiatr nie straszny. Balista pod kadłubem zadaje podwójne obrażenia; dwa działka automatyczne pod skrzydłami strzelają i biją 1,5 raza mocniej.',
 'Dwa wirniki na bocznych belkach i skarbiec zawieszony pod brzuchem. Spala paliwo, startuje pionowo i powoli przyspiesza.'])
L['tr_tr'] = (['Kargo Kuadrokopteri', 'Kargo Jirodini', 'Kargo Çift Kanatlısı', 'Kargo Deniz Uçağı', 'Gigantia', 'Pelikan', 'Şahin', 'Yusufçuk'], [
 'Quadrocopter tabanlı yavaş bir yük taşıyıcı. Rüzgârdan nefret eder.',
 'Kargo bölmesi ve motoru olan bir jirodin. Yakıt harcar, dikey kalkış yapar ve ileri hız kazanması biraz sürer.',
 'Koltukların yerinde sandıklar bulunan çift motorlu bir çift kanatlı uçak.',
 'Sandıklarını kabinin arkasında taşıyan bir uçan tekne.',
 'Altı motor ve bitmeyen kanatlar. Kolay havalanır, rüzgâra aldırmaz ve en çok yükü taşır.',
 'Dört motorunun da çalıştığı suyun üzerinde en hızlısı. Sadece kolu sertçe çekerseniz sudan ayrılır; havada yavaş ve beceriksizdir.',
 'Rüzgâra aldırmayan bir silahlı helikopter. Karın altındaki balista çift hasar verir; kanat altındaki iki otomatik top 1,5 kat daha sert ateş eder ve vurur.',
 'Yan kirişlerde iki rotor ve karnın altında asılı bir kasa. Yakıt harcar, dikey kalkış yapar ve yavaş hızlanır.'])
L['uk_ua'] = (['Вантажний квадрокоптер', 'Вантажний гіродин', 'Вантажний біплан', 'Вантажний гідролітак', 'Гігантія', 'Пелікан', 'Яструб', 'Бабка'], [
 'Повільний вантажівець на основі квадрокоптера. Ненавидить вітер.',
 'Гіродин із вантажним відсіком і двигуном. Витрачає пальне, злітає вертикально і не одразу набирає швидкість уперед.',
 'Двомоторний біплан зі скринями замість сидінь.',
 'Літальний човен, що возить скрині за кабіною.',
 'Шість двигунів і нескінченні крила. Легко злітає, ігнорує вітер і перевозить найбільше.',
 'Найшвидший над водою, де працюють усі чотири двигуни. Відривається від води, лише коли рішуче потягнути штурвал на себе, а в повітрі повільний і незграбний.',
 'Канонерка, якій байдужий вітер. Баліста під черевом завдає подвійної шкоди; дві автогармати під крилами стріляють і б’ють у 1,5 раза сильніше.',
 'Два гвинти на бічних балках і сховище під черевом. Витрачає пальне, злітає вертикально і повільно розганяється.'])
L['zh_cn'] = (['货运四旋翼机', '货运旋翼机', '货运双翼机', '货运水上飞机', '巨人号', '鹈鹕号', '猎鹰号', '蜻蜓号'], [
 '基于四旋翼机改造的慢速运输机。讨厌大风。',
 '带货舱和发动机的旋翼机。消耗燃料，可垂直起飞，向前加速较慢。',
 '座位处改装成箱子的双发双翼机。',
 '把箱子装在驾驶舱后方的飞行艇。',
 '六台发动机和望不到头的机翼。容易起飞，不受风影响，载货最多。',
 '在水面上最快，四台发动机全部工作。只有用力拉杆才会离水，在空中又慢又笨拙。',
 '不受风影响的武装直升机。机腹弩炮造成双倍伤害；机翼下的两门机炮射速与伤害均为1.5倍。',
 '两侧悬臂上各有一个旋翼，机腹下吊着一个保险库。消耗燃料，可垂直起飞，加速缓慢。'])
L['zh_tw'] = (['貨運四旋翼機', '貨運旋翼機', '貨運雙翼機', '貨運水上飛機', '巨人號', '鵜鶘號', '獵鷹號', '蜻蜓號'], [
 '以四旋翼機改造的慢速運輸機。討厭大風。',
 '附貨艙與引擎的旋翼機。消耗燃料，可垂直起飛，向前加速較慢。',
 '座位處改裝成箱子的雙發雙翼機。',
 '把箱子裝在駕駛艙後方的飛行艇。',
 '六具引擎與望不到盡頭的機翼。容易起飛，不受風影響，載貨最多。',
 '在水面上最快，四具引擎全部運作。只有用力拉桿才會離水，在空中又慢又笨拙。',
 '不受風影響的武裝直升機。機腹弩砲造成雙倍傷害；機翼下的兩門機砲射速與傷害皆為1.5倍。',
 '兩側懸臂上各有一個旋翼，機腹下吊著一座保險庫。消耗燃料，可垂直起飛，加速緩慢。'])
L['nl_nl'] = (['Vracht-quadrocopter', 'Vracht-gyrodyne', 'Vracht-dubbeldekker', 'Vracht-watervliegtuig', 'Gigantia', 'Pelikaan', 'Havik', 'Libelle'], [
 'Een trage vrachtvlieger gebaseerd op de Quadrocopter. Haat wind.',
 'Een gyrodyne met laadruim en motor. Verbruikt brandstof, stijgt verticaal op en heeft even nodig om vooruit snelheid te maken.',
 'Een tweemotorige dubbeldekker met kisten waar de stoelen waren.',
 'Een vliegboot die zijn kisten achter de cabine vervoert.',
 'Zes motoren en vleugels zonder einde. Stijgt makkelijk op, trekt zich niets van wind aan en vervoert het meest.',
 'Het snelst over water, waar alle vier de motoren draaien. Hij verlaat het water alleen als je stevig optrekt en is in de lucht traag en onhandig.',
 'Een gevechtshelikopter die wind negeert. De buikballista doet dubbele schade; de twee automatische kanonnen onder de vleugels vuren en raken 1,5 keer zo hard.',
 'Twee rotors op zijbalken en een kluis onder de buik. Verbruikt brandstof, stijgt verticaal op en versnelt langzaam.'])
L['sv_se'] = (['Fraktkvadrokopter', 'Fraktgyrodyn', 'Fraktbiplan', 'Fraktsjöflygplan', 'Gigantia', 'Pelikan', 'Hök', 'Trollslända'], [
 'En långsam lastbärare baserad på Quadrocoptern. Hatar vind.',
 'En gyrodyn med lastutrymme och motor. Förbrukar bränsle, lyfter lodrätt och tar en stund på sig att få fart framåt.',
 'Ett tvåmotorigt biplan med kistor där sätena satt.',
 'En flygbåt som bär sina kistor bakom kabinen.',
 'Sex motorer och vingar utan slut. Lyfter lätt, struntar i vind och bär mest.',
 'Snabbast över vatten, där alla fyra motorer går. Den lämnar bara vattnet om du drar ordentligt i spaken och är långsam och klumpig i luften.',
 'Ett attackflygplan som ignorerar vind. Ballistan under buken gör dubbel skada; de två automatkanonerna under vingarna skjuter och träffar 1,5 gånger hårdare.',
 'Två rotorer på sidobommar och ett valv hängande under buken. Förbrukar bränsle, lyfter lodrätt och accelererar långsamt.'])
L['cs_cz'] = (['Nákladní kvadrokoptéra', 'Nákladní autogyro', 'Nákladní dvouplošník', 'Nákladní hydroplán', 'Gigantia', 'Pelikán', 'Jestřáb', 'Vážka'], [
 'Pomalý nosič postavený na Quadrocopteru. Nesnáší vítr.',
 'Vírník s nákladním prostorem a motorem. Spotřebovává palivo, startuje kolmo a trvá mu, než nabere rychlost vpřed.',
 'Dvoumotorový dvouplošník s truhlami na místě sedadel.',
 'Létající člun, který vozí truhly za kabinou.',
 'Šest motorů a nekonečná křídla. Snadno vzlétne, vítr mu nevadí a unese nejvíc.',
 'Nejrychlejší nad vodou, kde běží všechny čtyři motory. Vodu opustí, jen když rázně zatáhnete za páku, a ve vzduchu je pomalý a nemotorný.',
 'Bitevní vrtulník, kterému vítr nevadí. Balista pod trupem způsobuje dvojnásobné poškození; dva automatické kanóny pod křídly střílejí i zasahují 1,5krát silněji.',
 'Dva rotory na bočních nosnících a trezor zavěšený pod břichem. Spotřebovává palivo, startuje kolmo a pomalu zrychluje.'])
L['hu_hu'] = (['Teher-kvadrokopter', 'Teher-girodin', 'Teher-kétfedelű', 'Teher-vízirepülő', 'Gigantia', 'Pelikán', 'Sólyom', 'Szitakötő'], [
 'Lassú teherszállító a Quadrocopter alapján. Utálja a szelet.',
 'Girodin raktérrel és motorral. Üzemanyagot fogyaszt, függőlegesen száll fel, és kell egy kis idő, mire előre felgyorsul.',
 'Kéthajtóműves kétfedelű, ülések helyett ládákkal.',
 'Repülőcsónak, amely a ládáit a fülke mögött viszi.',
 'Hat motor és véget nem érő szárnyak. Könnyen felszáll, nem törődik a széllel, és a legtöbbet szállítja.',
 'A leggyorsabb a vízen, ahol mind a négy motor működik. Csak határozott húzásra hagyja el a vizet, a levegőben lassú és esetlen.',
 'Szélre fittyet hányó csatahelikopter. A hasi ballista dupla sebzést okoz; a szárnyak alatti két gépágyú 1,5-szer erősebben lő és talál.',
 'Két rotor oldalsó gémeken és egy trezor a has alatt. Üzemanyagot fogyaszt, függőlegesen száll fel, és lassan gyorsul.'])
L['id_id'] = (['Kuadrokopter Kargo', 'Giroplane Kargo', 'Pesawat Bersayap Ganda Kargo', 'Pesawat Amfibi Kargo', 'Gigantia', 'Pelikan', 'Elang', 'Capung'], [
 'Pengangkut lambat berbasis Quadrocopter. Benci angin.',
 'Giroplane dengan ruang kargo dan mesin. Menghabiskan bahan bakar, lepas landas secara vertikal, dan butuh waktu untuk mencapai kecepatan maju.',
 'Pesawat bersayap ganda bermesin dua dengan peti di tempat kursi.',
 'Perahu terbang yang membawa petinya di belakang kabin.',
 'Enam mesin dan sayap yang tak ada habisnya. Mudah lepas landas, tak terpengaruh angin, dan membawa muatan terbanyak.',
 'Tercepat di atas air, tempat keempat mesinnya menyala. Hanya meninggalkan air jika tuas ditarik dengan tegas, dan lambat serta kikuk di udara.',
 'Helikopter tempur yang tak peduli angin. Balista di perut memberi dua kali lipat kerusakan; dua meriam otomatis di bawah sayap menembak dan menghantam 1,5 kali lebih keras.',
 'Dua rotor di balok samping dan brankas tergantung di bawah perut. Menghabiskan bahan bakar, lepas landas secara vertikal, dan berakselerasi lambat.'])
L['vi_vn'] = (['Trực thăng bốn cánh chở hàng', 'Trực thăng cánh quạt chở hàng', 'Máy bay hai tầng cánh chở hàng', 'Thủy phi cơ chở hàng', 'Gigantia', 'Bồ nông', 'Diều hâu', 'Chuồn chuồn'], [
 'Máy bay chở hàng chậm dựa trên Quadrocopter. Ghét gió.',
 'Một chiếc gyrodyne có khoang hàng và động cơ. Tốn nhiên liệu, cất cánh thẳng đứng và mất một lúc mới đạt tốc độ tiến.',
 'Máy bay hai tầng cánh hai động cơ, có rương ở chỗ ghế ngồi.',
 'Thuyền bay chở rương phía sau buồng lái.',
 'Sáu động cơ và đôi cánh dài vô tận. Dễ cất cánh, không sợ gió và chở được nhiều nhất.',
 'Nhanh nhất trên mặt nước, nơi cả bốn động cơ hoạt động. Chỉ rời mặt nước khi bạn kéo cần thật dứt khoát, và chậm chạp, vụng về trên không.',
 'Trực thăng chiến đấu không sợ gió. Ballista dưới bụng gây sát thương gấp đôi; hai khẩu pháo tự động dưới cánh bắn và đánh mạnh gấp 1,5 lần.',
 'Hai cánh quạt trên các dầm bên và một két sắt treo dưới bụng. Tốn nhiên liệu, cất cánh thẳng đứng và tăng tốc chậm.'])
L['th_th'] = (['ควอดโรคอปเตอร์ขนส่ง', 'ไจโรดายน์ขนส่ง', 'เครื่องบินปีกสองชั้นขนส่ง', 'เครื่องบินทะเลขนส่ง', 'ไจแกนเทีย', 'นกกระทุง', 'เหยี่ยว', 'แมลงปอ'], [
 'เครื่องขนส่งช้าที่สร้างจากควอดโรคอปเตอร์ เกลียดลม',
 'ไจโรดายน์ที่มีห้องสัมภาระและเครื่องยนต์ กินเชื้อเพลิง ขึ้นบินในแนวดิ่ง และใช้เวลาสักพักกว่าจะเร่งความเร็วไปข้างหน้า',
 'เครื่องบินปีกสองชั้นสองเครื่องยนต์ มีหีบอยู่ตรงที่นั่งเดิม',
 'เรือบินที่เก็บหีบไว้ด้านหลังห้องนักบิน',
 'เครื่องยนต์หกตัวและปีกที่ยาวไม่สิ้นสุด ขึ้นบินง่าย ไม่กลัวลม และบรรทุกได้มากที่สุด',
 'เร็วที่สุดบนผิวน้ำที่เครื่องยนต์ทั้งสี่ทำงาน จะพ้นน้ำก็ต่อเมื่อดึงคันบังคับแรง ๆ และช้าเก้งก้างเมื่ออยู่บนอากาศ',
 'เฮลิคอปเตอร์ติดอาวุธที่ไม่กลัวลม หน้าไม้ใต้ท้องสร้างความเสียหายสองเท่า ปืนใหญ่อัตโนมัติสองกระบอกใต้ปีกยิงและโจมตีแรงขึ้น 1.5 เท่า',
 'โรเตอร์สองตัวบนแขนด้านข้างและห้องนิรภัยห้อยใต้ท้อง กินเชื้อเพลิง ขึ้นบินในแนวดิ่ง และเร่งความเร็วช้า'])
L['ar_sa'] = (['مروحية رباعية للشحن', 'جيروداين للشحن', 'طائرة ثنائية السطح للشحن', 'طائرة مائية للشحن', 'غيغانتيا', 'البجعة', 'الصقر', 'اليعسوب'], [
 'ناقلة بطيئة مبنية على المروحية الرباعية. تكره الرياح.',
 'جيروداين مزودة بمقصورة شحن ومحرك. تستهلك الوقود، وتقلع عموديًا، وتحتاج بعض الوقت لاكتساب السرعة للأمام.',
 'طائرة ثنائية السطح بمحركين وصناديق مكان المقاعد.',
 'قارب طائر ينقل صناديقه خلف المقصورة.',
 'ستة محركات وأجنحة لا تنتهي. تقلع بسهولة، ولا تتأثر بالرياح، وتحمل أكبر حمولة.',
 'الأسرع فوق الماء حيث تعمل المحركات الأربعة كلها. لا تغادر الماء إلا إذا سحبت المقود بحزم، وهي بطيئة وخرقاء في الجو.',
 'مروحية قتالية لا تبالي بالرياح. تسبب المنجنيق تحت البطن ضعف الضرر؛ ويطلق المدفعان الآليان تحت الجناحين النار ويضربان بقوة أكبر بمقدار 1.5 مرة.',
 'مروحتان على عارضتين جانبيتين وخزنة معلقة تحت البطن. تستهلك الوقود، وتقلع عموديًا، وتتسارع ببطء.'])
L['fi_fi'] = (['Rahtikopteri', 'Rahtigyrodyne', 'Rahtikaksitaso', 'Rahtivesitaso', 'Gigantia', 'Pelikaani', 'Haukka', 'Sudenkorento'], [
 'Hidas rahdinkuljettaja Quadrocopterin pohjalta. Vihaa tuulta.',
 'Gyrodyne, jossa on lastiruuma ja moottori. Kuluttaa polttoainetta, nousee pystysuoraan ja kiihtyy eteenpäin hitaasti.',
 'Kaksimoottorinen kaksitaso, jossa on arkkuja istuinten paikalla.',
 'Lentävä vene, joka kuljettaa arkkunsa ohjaamon takana.',
 'Kuusi moottoria ja päättymättömät siivet. Nousee helposti, ei piittaa tuulesta ja kantaa eniten.',
 'Nopein vedellä, jossa kaikki neljä moottoria käyvät. Irtoaa vedestä vain, jos vedät ohjaussauvasta napakasti, ja ilmassa se on hidas ja kömpelö.',
 'Taisteluhelikopteri, joka ei piittaa tuulesta. Vatsan alla oleva ballista tekee kaksinkertaisen vahingon; kaksi siipien alla olevaa konetykkiä ampuu ja osuu 1,5 kertaa kovempaa.',
 'Kaksi roottoria sivupuomeissa ja holvi roikkumassa vatsan alla. Kuluttaa polttoainetta, nousee pystysuoraan ja kiihtyy hitaasti.'])
L['da_dk'] = (['Fragt-quadrocopter', 'Fragt-gyrodyne', 'Fragt-biplan', 'Fragt-søfly', 'Gigantia', 'Pelikan', 'Høg', 'Guldsmed'], [
 'En langsom lastbærer bygget på Quadrocopteren. Hader vind.',
 'En gyrodyne med lastrum og motor. Bruger brændstof, letter lodret og er længe om at få fart fremad.',
 'Et tomotoret biplan med kister, hvor sæderne var.',
 'En flyvebåd, der bærer sine kister bag kabinen.',
 'Seks motorer og vinger uden ende. Letter let, ænser ikke vind og bærer mest.',
 'Hurtigst over vand, hvor alle fire motorer kører. Den forlader kun vandet, hvis du trækker kraftigt op, og i luften er den langsom og kluntet.',
 'Et kampfly, der ignorerer vind. Ballistaen under maven gør dobbelt skade; de to automatkanoner under vingerne skyder og rammer 1,5 gange hårdere.',
 'To rotorer på sidebomme og et hvælv hængende under maven. Bruger brændstof, letter lodret og accelererer langsomt.'])
L['nb_no'] = (['Frakt-quadrokopter', 'Frakt-gyrodyne', 'Frakt-biplan', 'Frakt-sjøfly', 'Gigantia', 'Pelikan', 'Hauk', 'Øyenstikker'], [
 'En treg lastebærer bygget på Quadrocopteren. Hater vind.',
 'En gyrodyne med lasterom og motor. Bruker drivstoff, letter loddrett og bruker tid på å få fart framover.',
 'Et tomotors biplan med kister der setene var.',
 'En flybåt som bærer kistene bak kabinen.',
 'Seks motorer og vinger uten ende. Letter lett, bryr seg ikke om vind og bærer mest.',
 'Raskest over vann, der alle fire motorene går. Den forlater bare vannet hvis du drar fast opp, og i luften er den treg og klumpete.',
 'Et kampfly som ignorerer vind. Ballistaen under buken gjør dobbel skade; de to automatkanonene under vingene skyter og treffer 1,5 ganger hardere.',
 'To rotorer på sidebommer og hvelv hengende under buken. Bruker drivstoff, letter loddrett og akselererer sakte.'])
L['ro_ro'] = (['Cvadricopter de marfă', 'Girodină de marfă', 'Biplan de marfă', 'Hidroavion de marfă', 'Gigantia', 'Pelican', 'Șoim', 'Libelulă'], [
 'Un transportor lent construit pe Quadrocopter. Urăște vântul.',
 'O girodină cu cală și motor. Consumă combustibil, decolează vertical și îi ia ceva timp să prindă viteză înainte.',
 'Un biplan cu două motoare, cu lăzi în locul scaunelor.',
 'O navă zburătoare care își duce lăzile în spatele cabinei.',
 'Șase motoare și aripi fără sfârșit. Decolează ușor, ignoră vântul și duce cel mai mult.',
 'Cel mai rapid pe apă, unde funcționează toate cele patru motoare. Părăsește apa doar dacă tragi ferm de manșă și e lent și stângaci în aer.',
 'O canonieră care ignoră vântul. Balista de sub burtă face daună dublă; cele două tunuri automate de sub aripi trag și lovesc de 1,5 ori mai tare.',
 'Două rotoare pe brațe laterale și un seif atârnat sub burtă. Consumă combustibil, decolează vertical și accelerează încet.'])
L['el_gr'] = (['Φορτηγό τετρακόπτερο', 'Φορτηγό γυροπλάνο', 'Φορτηγό διπλάνο', 'Φορτηγό υδροπλάνο', 'Γιγαντία', 'Πελεκάνος', 'Γεράκι', 'Λιβελούλα'], [
 'Ένα αργό φορτηγό βασισμένο στο Quadrocopter. Μισεί τον άνεμο.',
 'Ένα γυροπλάνο με χώρο φορτίου και κινητήρα. Καταναλώνει καύσιμο, απογειώνεται κάθετα και αργεί να πάρει ταχύτητα προς τα εμπρός.',
 'Ένα διπλάνο με δύο κινητήρες και σεντούκια στη θέση των καθισμάτων.',
 'Ένα ιπτάμενο σκάφος που κουβαλά τα σεντούκια του πίσω από την καμπίνα.',
 'Έξι κινητήρες και φτερά που δεν τελειώνουν. Απογειώνεται εύκολα, αγνοεί τον άνεμο και μεταφέρει τα περισσότερα.',
 'Ο ταχύτερος πάνω από το νερό, όπου δουλεύουν και οι τέσσερις κινητήρες. Αφήνει το νερό μόνο αν τραβήξεις αποφασιστικά τον μοχλό και στον αέρα είναι αργός και αδέξιος.',
 'Ένα πολεμικό ελικόπτερο που αγνοεί τον άνεμο. Η βαλλίστρα κάτω από την κοιλιά προκαλεί διπλή ζημιά· τα δύο αυτόματα κανόνια κάτω από τα φτερά πυροβολούν και χτυπούν 1,5 φορά πιο δυνατά.',
 'Δύο έλικες σε πλευρικούς βραχίονες και ένα θησαυροφυλάκιο κρεμασμένο κάτω από την κοιλιά. Καταναλώνει καύσιμο, απογειώνεται κάθετα και επιταχύνει αργά.'])
L['he_il'] = (['קוואדרוקופטר מטען', 'ג׳יירודיין מטען', 'מטוס דו-כנפי למטען', 'מטוס ים למטען', 'גיגנטיה', 'שקנאי', 'נץ', 'שפירית'], [
 'מובילת מטען איטית המבוססת על הקוואדרוקופטר. שונאת רוח.',
 'ג׳יירודיין עם תא מטען ומנוע. צורך דלק, ממריא אנכית ולוקח לו זמן להאיץ קדימה.',
 'מטוס דו-כנפי דו-מנועי עם תיבות במקום המושבים.',
 'סירה מעופפת שנושאת את התיבות שלה מאחורי התא.',
 'שישה מנועים וכנפיים אינסופיות. ממריאה בקלות, מתעלמת מרוח ונושאת הכי הרבה.',
 'המהיר ביותר מעל המים, שם כל ארבעת המנועים פועלים. הוא עוזב את המים רק אם מושכים בחוזקה, ובאוויר הוא איטי וגמלוני.',
 'ספינת קרב שמתעלמת מרוח. הבליסטרה שמתחת לבטן גורמת לנזק כפול; שני תותחי האוטומט שמתחת לכנפיים יורים ופוגעים חזק פי 1.5.',
 'שני רוטורים על זרועות צד וכספת תלויה מתחת לבטן. צורך דלק, ממריא אנכית ומאיץ לאט.'])

def build(code, names, descs):
    d = {'itemGroup.ia_industries.aircraft': GROUP}
    for i, a in enumerate(IDS):
        d['item.ia_industries.' + a] = names[i]; d['item.ia_industries.%s.description' % a] = descs[i]; d['entity.ia_industries.' + a] = names[i]
    return d
if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for code, (n, ds) in L.items():
        assert len(n) == 8 and len(ds) == 8, code
        json.dump(build(code, n, ds), open('%s/%s.json' % (out, code), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print(len(L), 'languages')
