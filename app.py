import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

try:
    pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))
    pdfmetrics.registerFont(TTFont('Arial-Bold', 'arialbd.ttf'))
except:
    pass

st.set_page_config(
    page_title="Surat Pengantar RT",
    page_icon="📋",
    layout="centered"
)

st.title("📋 Sistem Surat Pengantar RT")
st.markdown("*Kelurahan Paropo, Kecamatan Panakkukang, Kota Makassar*")
st.markdown("---")

BULAN_ROMAWI = {
    1: 'JAN', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MEI', 6: 'JUN',
    7: 'JUL', 8: 'AGS', 9: 'SEP', 10: 'OKT', 11: 'NOV', 12: 'DES'
}
BULAN_INDO = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
              'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']

with st.form("surat_form"):
    st.subheader("📝 Nomor Surat (bagian bawah kanan)")
    st.caption("Format: Nomor / ORT (RT) / Bulan / Tahun — cth: 007/ORT 002/IX/2026")

    col1, col2 = st.columns(2)
    with col1:
        nomor_urut = st.text_input("Nomor*", placeholder="007")
    with col2:
        tanggal_surat = st.date_input("Tanggal Surat*", value=datetime.now())

    st.subheader("🏘️ Data Pengurus")
    col1, col2 = st.columns(2)
    with col1:
        rt_number = st.text_input("RT*", value="002", placeholder="002")
    with col2:
        rw_number = st.text_input("RW*", value="002", placeholder="002")

    col1, col2 = st.columns(2)
    with col1:
        nama_ketua_rt = st.text_input("Nama Ketua RT*", placeholder="RAHMAT MUSTAMIN")
    with col2:
        nama_ketua_rw = st.text_input("Nama Ketua RW*", placeholder="NURUL WAHDANIAH")

    st.subheader("👤 Data Warga")

    nama = st.text_input("Nama Lengkap*", placeholder="MULYANINGSIH")

    col1, col2 = st.columns(2)
    with col1:
        tempat_lahir = st.text_input("Tempat Lahir*", placeholder="JAKARTA PUSAT")
    with col2:
        tanggal_lahir = st.date_input("Tanggal Lahir*", value=datetime(1978, 4, 16))

    nik = st.text_input("NIK*", placeholder="7371096604780003")

    col1, col2 = st.columns(2)
    with col1:
        jenis_kelamin = st.selectbox("Jenis Kelamin*", ["LAKI-LAKI", "PEREMPUAN"])
    with col2:
        agama = st.selectbox("Agama*", ["ISLAM", "KRISTEN PROTESTAN", "KRISTEN KATOLIK", "HINDU", "BUDDHA", "KONGHUCU"])

    pekerjaan = st.text_input("Pekerjaan*", placeholder="IBU RUMAH TANGGA")
    alamat = st.text_input("Alamat Lengkap*", placeholder="BTN PAROPO BLOK B18")
    telepon = st.text_input("No. Telepon/HP*", placeholder="081355002101")

    st.subheader("📋 Tujuan Pengurusan (pilih yang sesuai)")

    tujuan_selected = {}

    # Kategori 1
    if st.checkbox("1. Formulir Pembuatan Kartu Keluarga (KK), Kartu Tanda Penduduk (KTP), Akta Kelahiran/Kematian, Pindah Alamat/Kedatangan", key="tujuan_1"):
        tujuan_selected[1] = "Formulir Pembuatan Kartu Keluarga (KK), Kartu Tanda Penduduk (KTP), Akta Kelahiran/Kematian, Pindah Alamat/Kedatangan"

    # Kategori 2
    if st.checkbox("2. Surat Pengantar Penerbitan/Keterangan Berkelakuan Baik (SKCK), Izin Keramaian", key="tujuan_2"):
        tujuan_selected[2] = "Surat Pengantar Penerbitan/Keterangan Berkelakuan Baik (SKCK), Izin Keramaian"

    # Kategori 3 - Sub kategori
    st.write("**3. Surat Keterangan ;**")
    sub_tujuan = {}
    sub_options = [
        ("a", "a. Domisili Penduduk"),
        ("b", "b. Pernah/Belum Pernah Menikah, Belum Bekerja, Belum Memiliki Rumah"),
        ("c", "c. Tidak/Kurang Mampu"),
        ("d", "d. Keterangan Penghasilan"),
        ("e", "e. Usaha, Domisili Usaha (Yayasan, Masjid, Gereja, Sekolah, dll)"),
        ("f", "f. Rekomendasi SITU-SIUP, IMB"),
        ("g", "g. Penerbitan SPPT PBB (SPOP), SPORADIK"),
        ("h", "h. Surat Pernyataan Ahli Waris/Kuasa Ahli Waris"),
        ("i", "i. Legalisir KTP, KK, Kematian, dll"),
    ]

    for key, label in sub_options:
        if st.checkbox(label, key=f"tujuan_3_{key}"):
            sub_tujuan[key] = label

    tujuan_custom = st.text_input("j. Lainnya (jika ada)", placeholder="……………………………………………")

    if sub_tujuan:
        tujuan_selected[3] = sub_tujuan
    if tujuan_custom.strip():
        tujuan_selected['custom'] = tujuan_custom.strip()

    submitted = st.form_submit_button("🖨️ Generate PDF", type="primary", use_container_width=True)

def generate_pdf(data):
    # Gunakan /tmp/ untuk ephemeral storage (cocok untuk Helipod)
    output_path = os.path.join('/tmp', f"Surat_Pengantar_{data['nomor_urut']}.pdf")

    # Reduce margins untuk fit 1 page
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.2*cm,
        bottomMargin=1.2*cm
    )

    # Ukuran font lebih kecil agar fit 1 halaman A4
    FS = 9  # base font size
    FL = 11  # leading (dikurangi)

    styles = {
        'center_bold': ParagraphStyle(
            'CenterBold', fontSize=FS, alignment=TA_CENTER,
            fontName='Helvetica-Bold', leading=FS+2,
        ),
        'center': ParagraphStyle(
            'Center', fontSize=FS-1, alignment=TA_CENTER,
            fontName='Helvetica', leading=FS+1,
        ),
        'left': ParagraphStyle(
            'Left', fontSize=FS, alignment=TA_LEFT,
            fontName='Helvetica', leading=FL,
        ),
        'left_hanging': ParagraphStyle(
            'LeftHanging', fontSize=FS, alignment=TA_LEFT,
            fontName='Helvetica', leading=FL,
            leftIndent=0.5*cm,      # geser teks lanjutan
            firstLineIndent=-0.5*cm,  # baris pertama (nomor) mundur
        ),
        'justify': ParagraphStyle(
            'Justify', fontSize=FS, alignment=TA_JUSTIFY,
            fontName='Helvetica', leading=FL,
        ),
        'right': ParagraphStyle(
            'Right', fontSize=FS, alignment=TA_RIGHT,
            fontName='Helvetica', leading=FL,
        ),
    }

    story = []
    rt = data['rt_number']
    rw = data['rw_number']
    page_w = A4[0] - 3*cm  # usable width

    # === KOP SURAT: Logo | ORT/ORW + Kelurahan + Kecamatan ===
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kop_logo.png")
    logo_cell = ""
    if os.path.exists(logo_path):
        logo_cell = Image(logo_path, width=1.5*cm, height=1.9*cm)

    kop_right = Paragraph(
        f"<b>ORGANISASI RUKUN TETANGGA ORT {rt}</b><br/>"
        f"<b>ORGANISASI RUKUN WARGA ORW {rw}</b><br/>"
        f"KELURAHAN PAROPO<br/>"
        f"KECAMATAN PANAKKUKANG",
        styles['center_bold']
    )

    # Logo lebih dekat ke text (0.5cm gap)
    kop_tbl = Table([[logo_cell, kop_right]], colWidths=[2.2*cm, page_w - 2.2*cm])
    kop_tbl.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, 0), 'RIGHT'),  # logo align kanan dalam cell-nya
        ('ALIGN', (1, 0), (1, 0), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (0, 0), 3),  # 3pt gap antara logo dan text
        ('RIGHTPADDING', (1, 0), (1, 0), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
    ]))
    story.append(kop_tbl)
    
    # Garis ganda horizontal
    from reportlab.lib import colors
    from reportlab.platypus import HRFlowable
    story.append(Spacer(1, 2*mm))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.black, spaceAfter=1*mm))
    story.append(HRFlowable(width="100%", thickness=0.5, color=colors.black, spaceBefore=0))
    story.append(Spacer(1, 0.4*cm))

    # === NOMOR BAWAH (format baru) ===
    bln = BULAN_ROMAWI[data['tanggal_surat'].month]
    thn = data['tanggal_surat'].year
    nomor_lengkap = f"{data['nomor_urut']}/ORT {rt}/{bln}/{thn}"
    tgl_str = f"{data['tanggal_surat'].day} {BULAN_INDO[data['tanggal_surat'].month-1]} {data['tanggal_surat'].year}"
    ttl_str = f"{data['tempat_lahir'].upper()} / {data['tanggal_lahir'].strftime('%d %B %Y').upper()}"

    # === HEADER: Nomor/Perihal kiri, Kepada YTH kanan (turun sejajar Perihal) ===
    nomor_atas_statis = "..... /ORT.0..../ORW.0..../SP/......../20...."
    
    # Kiri: Nomor, Perihal
    # Kanan: Kepada YTH (turun 2 baris, sejajar dengan baris Perihal)
    header_data = [
        [Paragraph(f"<b>Nomor</b> &nbsp;&nbsp; : &nbsp; {nomor_atas_statis}", styles['left']), ''],
        [Paragraph(f"<b>Perihal</b> : &nbsp; <b>Surat Pengantar</b>", styles['left']),
         Paragraph("<b>Kepada YTH</b>", styles['right'])],
        ['', Paragraph("<b>LURAH PAROPO</b>", styles['right'])],
        ['', Paragraph("<b>Di &nbsp;&nbsp; Makassar</b>", styles['right'])],
    ]
    
    header_table = Table(header_data, colWidths=[8.5*cm, 7*cm])
    header_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 0.6*cm))

    # === ISI SURAT ===
    isi_text = f"""Kami yang bertanda tangan ini adalah Ketua ORT. {rt} ORW.{rw} Kelurahan Paropo Kecamatan Panakkukang Kota Makassar menyatakan bahwa :"""
    story.append(Paragraph(isi_text, styles['justify']))
    story.append(Spacer(1, 0.3*cm))

    # Data warga table - tanpa baris "(Wajib diisi)"
    warga_data = [
        [Paragraph("<b>Nama</b>", styles['left']),
         Paragraph(f": &nbsp; {data['nama'].upper()}", styles['left'])],
        [Paragraph("<b>Tempat/Tanggal Lahir</b>", styles['left']),
         Paragraph(f": &nbsp; {ttl_str}", styles['left'])],
        [Paragraph("<b>NIK</b>", styles['left']),
         Paragraph(f": &nbsp; {data['nik']}", styles['left'])],
        [Paragraph("<b>Jenis Kelamin</b>", styles['left']),
         Paragraph(f": &nbsp; {data['jenis_kelamin'].upper()}", styles['left'])],
        [Paragraph("<b>Agama</b>", styles['left']),
         Paragraph(f": &nbsp; {data['agama'].upper()}", styles['left'])],
        [Paragraph("<b>Pekerjaan</b>", styles['left']),
         Paragraph(f": &nbsp; {data['pekerjaan'].upper()}", styles['left'])],
        [Paragraph("<b>A l a m a t</b>", styles['left']),
         Paragraph(f": &nbsp; {data['alamat'].upper()}", styles['left'])],
        [Paragraph("<b>Telepon</b>", styles['left']),
         Paragraph(f": &nbsp; {data['telepon']}", styles['left'])],
        ['', Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;RT.{rt} RW.{rw} Kel. Paropo Kec. Panakkukang Kota Makassar", styles['left'])],
    ]

    tabel_warga = Table(warga_data, colWidths=[5.2*cm, 9.8*cm])
    tabel_warga.setStyle(TableStyle([
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 1.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1.5),
    ]))
    story.append(tabel_warga)
    story.append(Spacer(1, 0.4*cm))

    # Tujuan
    tujuan_text = f"Benar adalah warga RW{rw}/RT{rt} Kelurahan Paropo yang akan mengurus ;"
    story.append(Paragraph(tujuan_text, styles['justify']))
    story.append(Spacer(1, 0.3*cm))

    # Format tujuan - bold hanya untuk yang dipilih
    if 1 in data['tujuan']:
        story.append(Paragraph(f"<b>1. {data['tujuan'][1]}</b>", styles['left_hanging']))
    else:
        story.append(Paragraph("1. Formulir Pembuatan Kartu Keluarga (KK), Kartu Tanda Penduduk (KTP), Akta Kelahiran/Kematian, Pindah Alamat/Kedatangan", styles['left_hanging']))

    if 2 in data['tujuan']:
        story.append(Paragraph(f"<b>2. {data['tujuan'][2]}</b>", styles['left_hanging']))
    else:
        story.append(Paragraph("2. Surat Pengantar Penerbitan/Keterangan Berkelakuan Baik (SKCK), Izin Keramaian", styles['left_hanging']))

    # 3. Surat Keterangan ; (selalu tampil)
    story.append(Paragraph("3. Surat Keterangan ;", styles['left_hanging']))

    sub_items = [
        "a. Domisili Penduduk",
        "b. Pernah/Belum Pernah Menikah, Belum Bekerja, Belum Memiliki Rumah",
        "c. Tidak/Kurang Mampu",
        "d. Keterangan Penghasilan",
        "e. Usaha, Domisili Usaha (Yayasan, Masjid, Gereja, Sekolah, dll)",
        "f. Rekomendasi SITU-SIUP, IMB",
        "g. Penerbitan SPPT PBB (SPOP), SPORADIK",
        "h. Surat Pernyataan Ahli Waris/Kuasa Ahli Waris",
        "i. Legalisir KTP, KK, Kematian, dll",
    ]
    sub_map = {k.split('. ')[0]: k for k in sub_items}
    if 3 in data['tujuan']:
        selected_sub = data['tujuan'][3]
        for key in sorted(sub_map.keys()):
            item = sub_map[key]
            if key in selected_sub:
                story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;<b>{item}</b>", styles['left']))
            else:
                story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{item}", styles['left']))
        if 'custom' in data['tujuan']:
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;<b>j. {data['tujuan']['custom']}</b>", styles['left']))
        else:
            story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;j. …………………………………………………………………", styles['left']))
    else:
        for item in sub_items:
            story.append(Paragraph(f"&nbsp;&nbsp;&nbsp;&nbsp;{item}", styles['left']))
        story.append(Paragraph("&nbsp;&nbsp;&nbsp;&nbsp;j. …………………………………………………………………", styles['left']))

    story.append(Spacer(1, 0.5*cm))

    # Penutup
    penutup = """Demikian Surat Pengantar ini diberikan kepada yang bersangkutan untuk dipergunakan sebagaimana mestinya."""
    story.append(Paragraph(penutup, styles['justify']))
    story.append(Spacer(1, 0.3*cm))

    # Nomor dan Tanggal bawah (format formal - hanging indent)
    # Gunakan leftIndent agar teks lanjutan sejajar dengan margin teks
    style_hanging = ParagraphStyle(
        'HangingRight',
        parent=styles['right'],
        leftIndent=2*cm,      # geser seluruh paragraf
        firstLineIndent=-2*cm,  # baris pertama lebih kiri
    )
    story.append(Paragraph(f"<b>Nomor</b>   : {nomor_lengkap}", style_hanging))
    story.append(Paragraph(f"<b>Tanggal</b> : {tgl_str}", style_hanging))
    story.append(Spacer(1, 1*cm))

    # Tanda tangan dengan garis bawah nama (rapat: hanya 1 baris kosong)
    tt_data = [
        [Paragraph(f"<b>KETUA ORW {rw}</b>", styles['center']),
         Paragraph(f"<b>KETUA ORT{rt}/ORW{rw}</b>", styles['center'])],
        ['', ''],
        [Paragraph("<u>{nama_rw}</u>".format(nama_rw=data['nama_rw'].upper()), styles['center']),
         Paragraph("<u>{nama_rt}</u>".format(nama_rt=data['nama_rt'].upper()), styles['center'])],
    ]

    tabel_tt = Table(tt_data, colWidths=[7*cm, 7*cm])
    tabel_tt.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(tabel_tt)
    
    # Nama dengan garis bawah
    nama_rw = data['nama_ketua_rw'].upper()
    nama_rt = data['nama_ketua_rt'].upper()
    
    # Tabel nama dengan garis bawah
    nama_tbl = Table([
        [Paragraph(f"<u><b>({nama_rw})</b></u>", styles['center']),
         Paragraph(f"<u><b>({nama_rt})</b></u>", styles['center'])],
    ], colWidths=[7*cm, 7*cm])
    nama_tbl.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(nama_tbl)
    story.append(Spacer(1, 0.5*cm))

    # Catatan (Cat → Catatan, spasi setelah bullet)
    catatan = [
        "<b>Catatan :</b>",
        "Surat Pengantar diberikan jika melengkapi :",
        "• &nbsp; Pelunasan Pembayaran Sampah Tiap Bulan",
        "• &nbsp; Pelunasan Pembayaran PBB tahun berjalan",
        "• &nbsp; Lampirkan fotocopy KK dan KTP",
    ]
    for c in catatan:
        story.append(Paragraph(c, styles['left']))

    doc.build(story)
    return output_path, nomor_lengkap


if submitted:
    errors = []
    if not nomor_urut.strip():
        errors.append("Nomor wajib diisi")
    if not rt_number.strip():
        errors.append("RT wajib diisi")
    if not rw_number.strip():
        errors.append("RW wajib diisi")
    if not nama_ketua_rt.strip():
        errors.append("Nama Ketua RT wajib diisi")
    if not nama_ketua_rw.strip():
        errors.append("Nama Ketua RW wajib diisi")
    if not nama.strip():
        errors.append("Nama Lengkap wajib diisi")
    if not tempat_lahir.strip():
        errors.append("Tempat Lahir wajib diisi")
    if not nik.strip():
        errors.append("NIK wajib diisi")
    if len(nik.strip()) != 16:
        errors.append("NIK harus 16 digit")
    if not pekerjaan.strip():
        errors.append("Pekerjaan wajib diisi")
    if not alamat.strip():
        errors.append("Alamat wajib diisi")
    if not telepon.strip():
        errors.append("Telepon wajib diisi")
    if not tujuan_selected and not tujuan_custom.strip():
        errors.append("Pilih minimal satu Tujuan Pengurusan")

    if errors:
        for e in errors:
            st.error(e)
    else:
        data = {
            'nomor_urut': nomor_urut.strip(),
            'rt_number': rt_number.strip(),
            'rw_number': rw_number.strip(),
            'nama_ketua_rt': nama_ketua_rt.strip(),
            'nama_ketua_rw': nama_ketua_rw.strip(),
            'nama': nama.strip(),
            'tempat_lahir': tempat_lahir.strip(),
            'tanggal_lahir': tanggal_lahir,
            'nik': nik.strip(),
            'jenis_kelamin': jenis_kelamin,
            'agama': agama,
            'pekerjaan': pekerjaan.strip(),
            'alamat': alamat.strip(),
            'telepon': telepon.strip(),
            'tujuan': tujuan_selected,
            'tanggal_surat': tanggal_surat,
        }

        with st.spinner("Generating PDF..."):
            try:
                pdf_path, nomor_lengkap = generate_pdf(data)
                st.success("✅ PDF berhasil dibuat!")

                with open(pdf_path, 'rb') as f:
                    pdf_data = f.read()

                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_data,
                    file_name=f"Surat_Pengantar_RT_{nomor_urut}_{nama.replace(' ', '_')}.pdf",
                    mime='application/pdf',
                    use_container_width=True
                )

                st.info(f"""
                **Detail Surat:**
                - **Nomor (bawah):** {nomor_lengkap}
                - **Nama:** {nama.upper()}
                - **NIK:** {nik}
                - **RT/RW:** {rt_number}/{rw_number}
                - **Ketua RT:** {nama_ketua_rt.upper()}
                - **Ketua RW:** {nama_ketua_rw.upper()}
                """)

            except Exception as e:
                st.error(f"Error generating PDF: {str(e)}")

st.markdown("---")
st.caption("© 2026 ORT/ORW - Kelurahan Paropo | Sistem Surat Pengantar Otomatis")
