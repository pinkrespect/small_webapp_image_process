source ../necronomicon/necronomicon/bin/activate
# 만약 가상환경이 없는 경우 설치 핸들링
# python 버전 맞는지 확인
echo "activate virtual environment done"
echo "run python styletransfer.py"
echo "wait for done message...."

python ../necronomicon/styleTransfer.py uploaded_images/image.png uploaded_images/stylized.png 0.5 && echo "done"

echo "Success"
rm uploaded_images/*.*

