# Sik kullanilan komutlar
#
# Kullanim:
#     make            Yardim gosterir
#     make tumu       Butun analizleri sirayla calistirir
#     make temiz      Uretilen butun ciktilari siler
#
# Windows kullaniyorsaniz ve make kurulu degilse, komutlari
# dogrudan terminale yazabilirsiniz. Her satirin karsiligi asagida gorunuyor.

PYTHON := python

.PHONY: yardim tumu veri analiz01 analiz02 analiz03 makale temiz kontrol

yardim:
	@echo "Kullanilabilir komutlar:"
	@echo "  make veri       Ornek veriyi uretir"
	@echo "  make analiz01   Vektor saha verisi analizini calistirir"
	@echo "  make analiz02   Raster analizini calistirir"
	@echo "  make analiz03   Sismoloji analizini calistirir"
	@echo "  make tumu       Veri uretimi dahil hepsini sirayla calistirir"
	@echo "  make makale     Makaleyi PDF olarak derler (quarto gerekir)"
	@echo "  make temiz      Uretilen butun ciktilari siler"
	@echo "  make kontrol    Ortamin dogru kurulup kurulmadigini kontrol eder"

veri:
	$(PYTHON) analizler/00_ornek_veri_uret.py

analiz01:
	$(PYTHON) analizler/01_vektor_saha_verisi.py

analiz02:
	$(PYTHON) analizler/02_raster_uydu_goruntusu.py

analiz03:
	$(PYTHON) analizler/03_sismoloji_zaman_serisi.py

tumu: veri analiz01 analiz02 analiz03
	@echo ""
	@echo "Butun analizler tamamlandi."
	@echo "Sekiller: sekiller/  Tablolar: ciktilar/"

makale:
	quarto render makale/makale.qmd --to pdf

temiz:
	rm -rf sekiller/*.png ciktilar/*.csv ciktilar/*.txt
	rm -rf veri/islenmis/*
	find . -type d -name __pycache__ -exec rm -rf {} +
	@echo "Uretilen ciktilar silindi. 'make tumu' ile yeniden uretebilirsiniz."

kontrol:
	@$(PYTHON) -c "import sys; print('Python', sys.version.split()[0])"
	@$(PYTHON) -c "import numpy, pandas, matplotlib; print('temel yigin: tamam')"
	@$(PYTHON) -c "import geopandas, rasterio, pyproj, shapely; print('mekansal: tamam')"
	@$(PYTHON) -c "import obspy; print('sismoloji: tamam')"
	@echo "Ortam kullanima hazir."
