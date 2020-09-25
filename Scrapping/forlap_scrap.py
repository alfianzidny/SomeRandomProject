from bs4 import BeautifulSoup
import requests
import re

def main():
    s = requests.session()
    url = "https://forlap.ristekdikti.go.id/mahasiswa"
    result = s.get(url)

    #bypass validasi captcha dan set variabel utk search
    captcha1 = BeautifulSoup(result.text, 'html.parser').find("input", {"name":"captcha_value_1"}).get('value')
    captcha2 = BeautifulSoup(result.text, 'html.parser').find("input", {"name":"captcha_value_2"}).get('value')

    params = {
        "dummy" :"031038+++Universitas+Bina+Nusantara",
        "id_sp" : "6C91755E-50E5-4ACF-B454-37A058BA9BCB",
        "id_sms" : "CA5901CA-D995-4A47-9D33-B46100A3E129",
        "keyword" : "2301",
        "kode_pengaman" : str(int(captcha1)+int(captcha2)),
        "captcha_value_1" : captcha1,
        "captcha_value_2" : captcha2
    }

    url = url + "/search/"

    # deklarasi untuk write to file

    #file binusian B23
    filename = "DataMahasiswaIT_B23.csv"
    f = open(filename, "w")
    
    filename2 = "wordlist1"
    f2 = open(filename2,"w")

    #deklarasi header di dalam file
    headers = "Nama, Jenis Kelamin, Perguruan Tinggi, Program Studi, Nomor Induk, Semester Awal, Status Awal, Status saat ini, Semester, Status, SKS, Semester, Status, SKS, Semester, Status, SKS\n"
    f.write(headers)

    #looping buat pages

    flag = 20
    for i in range (0,10000,20):
        #untuk load page berikutnya
        j = str(i)
        url1 = url + j
        
        s.post(url1, data=params)
        result = s.get(url1)

        #ambil data didalam keseluruhan page
        result = BeautifulSoup(result.text, "html.parser").find_all("tr", {"class":"tmiddle"})
        
        # ambil data di dalam tabel mahasiswa
        for link in result:
            # ambil isi yang ada di dalam href table
            data = link.find("a")["href"]

            url1 = requests.get(data)
            soup_page = BeautifulSoup(url1.text, 'lxml')

            container = soup_page.find_all("div", {"class":"main"})

            #akses data pribadi
            for data_umum in container:
                table_conn = data_umum.find("table", {"class":"table1"})
                row = table_conn.find_all("tr")
                
                if row[5]:
                    cell = row[5].find_all("td")
                    x = re.search("^(2301).\d+", cell[2].text)
                    if x:
                        print("="*30)
                    else:
                        print("--"*30)
                        pass
                #ambil data di row td
                if row[0]:
                    cell = row[0].find_all("td")
                    nama = cell[2].text
                    print("Nama: " + nama)
                if row[1]:
                    cell = row[1].find_all("td")
                    gender = cell[2].text
                    print("Jenis Kelamin: " + gender)
                if row[3]:
                    cell = row[3].find_all("td")
                    univ = cell[2].text
                    print("Universitas: " + univ)
                if row[4]:
                    cell = row[4].find_all("td")
                    program = cell[2].text
                    print("Program Studi: "+program)
                if row[5]:
                    cell = row[5].find_all("td")
                    nim = cell[2].text
                    print("Nomor Induk Mahasiswa: "+nim)
                if row[6]:
                    cell = row[6].find_all("td")
                    semawal = cell[2].text.strip()
                    print("Semester Awal: " + semawal)
                if row[7]:
                    cell = row[7].find_all("td")
                    statawal = cell[2].text.strip()
                    print("Status Awal Mahasiswa: "+statawal)
                if row[8]:
                    cell = row[8].find_all("td")
                    statnow = cell[2].text.strip()
                    print("Status Mahasiswa Sekarang: "+statnow)

                f.write(nama + "," + gender + "," + univ + "," + program + "," + nim + "," + semawal + "," + statawal + "," + statnow + ",")
                f2.write(nama + "," + nim)
            # print("x"*20) #data di tabel atas selesai

            container_1 = soup_page.find("div",{"id":"kuliahmhs"})
            datas = container_1.find_all("tr", {"class":"tmiddle"})

            try:
                for data_klh in datas:
                    data_mhs = data_klh.find_all("td")
                    semes = data_mhs[1].text
                    status = data_mhs[2].text
                    sks = data_mhs[3].text

                    print("Semester: "+semes+"\nStatus: "+status+"\nSKS: "+sks)
                    f.write(semes + "," + status + "," + sks + ",")
            except:
                pass
            # print("v"*20)

            container_2 = soup_page.find("div", {"id":"khsmhs"})
            riwayat = container_2.find_all("tr", {"class":"tmiddle"})

            try:
                for riw_klh in riwayat:
                    riw_mhs = riw_klh.find_all("td")
                    sms = riw_mhs[1].text
                    kode = riw_mhs[2].text
                    matkul = riw_mhs[3].text
                    jlhsks = riw_mhs[4].text

                    print("Semester: "+sms+"\nKode Mata Kuliah: "+kode+"\nMata Kuliah: "+matkul+"\nJumlah SKS: "+sks)
                    f.write(sms + "," + kode + "," + matkul + "," + jlhsks)

                f.write("\n")
                f2.write("\n")
            except:
                f.write("\n")
                f2.write("\n")
                pass
        print(flag)
        flag = flag+20
            # print("="*30)
    f.close()

if __name__ == "__main__":
    main()