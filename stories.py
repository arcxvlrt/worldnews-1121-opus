"""Stories for the 21 Nov 2026 page. Facts and source URLs are in NOTES.md.
conf: "2+" = two or more outlets, "OFF" = on the record from an authority, "ONE" = one outlet, "CLAIM" = one side's claim.
pin: (lon, lat) on the map, or None. "(Fri)" marks events of Fri 20 Nov (local time) first reported on the 21st."""

REGIONS = [("Europe", (36, 84, 160), 7), ("Asia", (186, 52, 42), 6), ("Middle East", (172, 108, 20), 6),
           ("Africa", (28, 118, 66), 4), ("Americas", (108, 62, 148), 6), ("Oceania", (14, 120, 132), 5),
           ("Global", (84, 88, 98), 3)]

DECK = ("COP31 talks run into Saturday  ·  Three Houthi missiles downed over Riyadh  ·  "
        "Russia fires 148 drones at Ukraine")

NUMBERS = [
    ("148", "drones fired at Ukraine; 117 downed or jammed"),
    ("3", "Houthi missiles intercepted over Riyadh"),
    ("6.7", "magnitude of the deep quake in central Peru"),
    ("146", "people safe after Davao emergency landing"),
    ("$57,000", "bitcoin falls below, first time since 2024"),
    ("136", "KL Rahul's innings in the Wellington Test"),
]

LEADS = [
    dict(n=1, region="Global", art="climate_talks", tag="NO DEAL YET", conf="2+", pin=(30.7, 36.9),
         label="ANTALYA, TÜRKIYE · CLIMATE",
         head="COP31 climate talks run into Saturday with no deal",
         body="Delegates argued through the night over a draft with no move away from fossil fuels; "
              "a new text is expected on Saturday.",
         src="BBC, Euronews, RTÉ"),
    dict(n=2, region="Middle East", art="missiles_night", tag="3 DOWNED", conf="OFF", pin=(46.7, 24.7),
         label="RIYADH, SAUDI ARABIA · WAR",
         head="Coalition downs three Houthi missiles aimed at Riyadh",
         body="A third straight day of alerts in the capital; a drone heading for the south was also "
              "destroyed, the Saudi-led coalition said.",
         src="AFP, Al Jazeera"),
    dict(n=3, region="Europe", art="strike_building", tag="148 DRONES", conf="OFF", pin=(33.4, 47.9),
         label="UKRAINE · WAR",
         head="Russia fires 3 missiles and 148 drones at Ukraine",
         body="The air force says 117 drones were downed or jammed. In Kryvyi Rih, Friday's strike toll rose to "
              "58 hurt; a boy of 7 and a paramedic died.",
         src="Ukrainska Pravda"),
]

CARDS = [
    dict(n=4, region="Global", art="robot", tag="NO BAN", conf="2+", pin=(6.1, 46.2),
         label="GENEVA · ARMS CONTROL", head="Killer-robot talks end without a binding ban",
         body="128 states agree on two more years of work.", src="DW, AP"),
    dict(n=5, region="Middle East", art="tanker", tag="2 TANKERS HIT", conf="OFF", pin=(56.2, 26.2), off=(8, 10),
         label="OFF OMAN · SHIPPING", head="Two tankers hit by unknown projectiles",
         body="North and east of Khasab; no injuries.", src="UKMTO"),
    dict(n=6, region="Asia", art="plane", tag="146 SAFE", conf="OFF", pin=(125.6, 7.1),
         label="DAVAO · AVIATION", head="Air Niugini jet lands after engine fire alert",
         body="All aboard left by slides after midnight.", src="CAAP, AP"),
    dict(n=7, region="Oceania", art="cricket", tag="RAHUL 136", conf="ONE", pin=(174.8, -41.3),
         label="WELLINGTON · CRICKET", head="India lead New Zealand by 118 runs",
         body="India 488/4 in reply to 368, day three.", src="RNZ"),
    dict(n=8, region="Global", art="coins", tag="BELOW $57,000", conf="ONE", pin=None,
         label="WORLD · CRYPTO", head="Bitcoin falls below $57,000",
         body="First time since Sept 2024; $2.4bn liquidated.", src="CoinDesk"),
    dict(n=9, region="Africa", art="boat", tag="4 DEAD", conf="OFF", pin=(6.1, 4.9),
         label="BAYELSA, NIGERIA · DISASTER", head="State warns boat crews after mourners drown",
         body="(Fri) Capsize kills 4; 24 people rescued.", src="Punch"),
    dict(n=10, region="Americas", art="gavel", tag="GUILTY", conf="OFF", pin=(-118.5, 34.05), off=(-12, 6),
         label="LOS ANGELES · COURTS", head="Retrial convicts man of starting Palisades fire",
         body="(Fri) The fire killed 12; sentencing 17 March.", src="BBC"),
    dict(n=11, region="Americas", art="racecar", tag="POLE: VERSTAPPEN", conf="ONE", pin=(-115.2, 36.1), off=(6, -10),
         label="LAS VEGAS · FORMULA 1", head="Antonelli fastest, Verstappen gets pole",
         body="(Fri night) Antonelli has a 5-place grid penalty.", src="The Race"),
    dict(n=12, region="Oceania", art="cyclone", tag="EMERGENCY", conf="OFF", pin=(-165.4, -11.6),
         label="COOK ISLANDS · STORM", head="Cyclone Xavier: emergency for Nassau",
         body="Now category 1; NZ air force flies in supplies.", src="RNZ"),
    dict(n=13, region="Americas", art="seismo", tag="M6.7", conf="OFF", pin=(-76.0, -10.9),
         label="JUNÍN, PERU · EARTHQUAKE", head="Deep 6.7 quake shakes central Peru",
         body="00:09 UTC, 108 km deep; no damage at first.", src="USGS, AP"),
]

BRIEFS = [
    (14, "Vinnytsia", "Strike on energy site cuts power in city", "Ukr. Pravda", "Europe"),
    (15, "Estonia", "NATO jets scrambled over drone threat", "Ukr. Pravda", "Europe"),
    (16, "London", "Miliband: EU reset goes ahead without fees deal", "BBC, RTÉ", "Europe"),
    (17, "Paris", "Sixth Saturday of cost-of-living protests", "France 24", "Europe"),
    (18, "Munich", "Kane out for months with ankle ligament tear", "AP", "Europe"),
    (19, "Bordeaux", "Loneliness tied to 38% higher dementia risk", "Euronews", "Europe"),
    (20, "Hormuz", "IRGC claims it downed a US MQ-9; unverified", "MEE", "Middle East"),
    (21, "Basra", "Power station fire kills 4, injures 35", "Al Jazeera", "Middle East"),
    (22, "Cairo", "Egypt says it presses Hamas to hand over arms", "Arab News", "Middle East"),
    (23, "Israel", "Woman in her 30s dies of rabies", "Times of Israel", "Middle East"),
    (24, "Manipur", "Toxic liquor kills 11; 180+ in hospital", "AFP", "Asia"),
    (25, "Taipei", "Cabinet calls 6.2% stock plunge short-term", "Focus Taiwan", "Asia"),
    (26, "Seoul", "Lee offers 100m-won exam-cheating reward", "Korea Herald", "Asia"),
    (27, "Beijing", "Singapore's Wong meets Li Qiang; 20+ deals due", "CNA", "Asia"),
    (28, "Bangkok", "Urgent meeting on toxic northern rivers", "Nation", "Asia"),
    (29, "Cricket Aus.", "Board backs captain Cummins", "ABC, RNZ", "Oceania"),
    (30, "Tocumwal", "Four festivalgoers struck by lightning", "ABC", "Oceania"),
    (31, "Melbourne", "Poll: Labor trails 43-57 before Victoria vote", "ABC", "Oceania"),
    (32, "Brasília", "(Fri) Jailed Bolsonaro in hospital", "DW", "Americas"),
    (33, "Missouri", "(Fri) Judge backs $7.25bn Roundup deal", "DW", "Americas"),
    (34, "Sinaloa", "(Fri) Media report capture of FBI fugitive", "CNN", "Americas"),
    (35, "South Africa", "ANC races to form city coalitions", "BBC", "Africa"),
    (36, "Obituary", "(Fri) Mlambo-Ngcuka, SA ex-deputy leader, dies", "AP", "Africa"),
    (37, "SA police", "(Fri) 581 women killed in three months", "Premium Times", "Africa"),
]

DATECHECK = ("Kept off this page because they broke before Saturday: the Wall Street correction (Fri close), "
             "Russian missiles over Poland, the UK–EU reset deal and the Iraqi push into Jurf al-Sakhar (Fri 20 Nov); "
             "the ICJ ruling on Myanmar and the Shenzhen summit (Thu 19 Nov). Still unconfirmed at press time: "
             "BepiColombo entering Mercury orbit and any final COP31 deal. "
             "(Fri) marks events of Fri 20 Nov local time first reported on Saturday.")

FOOTER = ("LABELS: 2+ OUTLETS = confirmed by two or more outlets · OFFICIAL = on the record from an authority · "
          "ONE OUTLET = single report · CLAIM = one side's account  ·  Original drawings · Map: Natural Earth")
