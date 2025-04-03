import os
from PyPDF2 import PdfMerger

# PDF 파일이 있는 폴더 경로
folder_path = '/Users/minheepark/Desktop/minhee/커서/PDF 합치기/테스트 폴더'  # 본인 폴더 경로로 수정

# 폴더 내 모든 PDF 파일을 리스트로 정리 (정렬 포함)
pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.pdf')])

merger = PdfMerger()

for pdf in pdf_files:
    full_path = os.path.join(folder_path, pdf)
    merger.append(full_path)
    print(f'✔️ 추가됨: {pdf}')

# 저장할 파일 경로
output_path = os.path.join(folder_path, 'merged_output.pdf')
merger.write(output_path)
merger.close()

print(f'\n✅ 완료! 저장 위치: {output_path}')
