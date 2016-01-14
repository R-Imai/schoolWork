#include <iostream>
#include <opencv2/opencv.hpp>
#include <opencv2/opencv.hpp>
using namespace cv;
using namespace std;

VideoCapture cap(0);
Mat img;
double criteria = 0;
double radius = 0; 


void Mouse(int event, int x, int y, int flags, void *param = NULL)
{
	long sum;
	switch (event)
	{
	case CV_EVENT_LBUTTONDOWN:
		cv::Vec3b* ptr = img.ptr<cv::Vec3b>(y);
		cv::Vec3b bgr = ptr[x];
		sum = bgr[0] * bgr[0] + bgr[1] * bgr[1] + bgr[2] * bgr[2];
		criteria = radius;
		//printf("(%d,%d):BGR=(%d,%d,%d)	sum=%ld \n", x, y, bgr[0], bgr[1], bgr[2], sum);
		cout << "(" << x << ", " << y << ")" << ":" << criteria << "\n";
		break;


	}
}

int main(int argc, const char *argv[]){
	long sum;
	int hist_g[256];
	int histB[256], histG[256], histR[256];
	int face[] = { cv::FONT_HERSHEY_SIMPLEX, cv::FONT_HERSHEY_PLAIN, cv::FONT_HERSHEY_DUPLEX, cv::FONT_HERSHEY_COMPLEX,
		cv::FONT_HERSHEY_TRIPLEX, cv::FONT_HERSHEY_COMPLEX_SMALL, cv::FONT_HERSHEY_SCRIPT_SIMPLEX,
		cv::FONT_HERSHEY_SCRIPT_COMPLEX, cv::FONT_ITALIC };
	

	if (!cap.isOpened())
		return (-1);//open error
	while (waitKey(1) != 'q'){
		for (int i = 0; i < 256; i++){
			hist_g[i] = 0;
			histB[i] = 0;
			histG[i] = 0;
			histR[i] = 0;
		}
		//cv::Mat hist_img(cv::Size(256, 256), CV_8UC3, cv::Scalar::all(255));
		cv::Mat histB_img(cv::Size(256, 256), CV_8UC3, cv::Scalar::all(255));
		cv::Mat histG_img(cv::Size(256, 256), CV_8UC3, cv::Scalar::all(255));
		cv::Mat histR_img(cv::Size(256, 256), CV_8UC3, cv::Scalar::all(255));
		cap >> img;
		if (img.empty()) continue;


		double scale = 4.0;
		cv::Mat gray, smallImg(cv::saturate_cast<int>(img.rows / scale), cv::saturate_cast<int>(img.cols / scale), CV_8UC1);
		// グレースケール画像に変換
		cv::cvtColor(img, gray, CV_BGR2GRAY);
		// 処理時間短縮のために画像を縮小
		cv::resize(gray, smallImg, smallImg.size(), 0, 0, cv::INTER_LINEAR);
		cv::equalizeHist(smallImg, smallImg);

		// 分類器の読み込み
		std::string cascadeName = "C:/Users/cit/Downloads/opencv-2.4.9/sources/data/haarcascades/haarcascade_frontalface_alt.xml"; // Haar-like
		//std::string cascadeName = "./lbpcascade_frontalface.xml"; // LBP
		cv::CascadeClassifier cascade;
		if (!cascade.load(cascadeName)){
			printf("error2\n");
			return -1;
		}

		std::vector<cv::Rect> faces;
		// マルチスケール（顔）探索
		// 画像，出力矩形，縮小スケール，最低矩形数，（フラグ），最小矩形
		cascade.detectMultiScale(smallImg, faces, 1.1, 2, CV_HAAR_SCALE_IMAGE, cv::Size(30, 30));
		// 結果の描画
		std::vector<cv::Rect>::const_iterator r = faces.begin();
		radius = 0;
		for (; r != faces.end(); ++r) {
			cv::Point center;
			//int radius;
			center.x = cv::saturate_cast<int>((r->x + r->width*0.5)*scale);
			center.y = cv::saturate_cast<int>((r->y + r->height*0.5)*scale);
			radius = cv::saturate_cast<int>((r->width + r->height)*0.25*scale);
			cv::circle(img, center, (int) radius, cv::Scalar(80, 80, 255), 3, 8, 0);
		}
		for (int y = 0; y < img.rows; y++) {
			cv::Vec3b* ptr = img.ptr<cv::Vec3b>(y);
			for (int x = 0; x < img.cols; x++) {
				int blight = img.at<unsigned char>(y, x);
				cv::Vec3b bgr = ptr[x];
				hist_g[blight]++;
				histB[bgr[0]]++;
				histG[bgr[1]]++;
				histR[bgr[2]]++;

			}

		}
		for (int n = 0; n <= 256; n++) {
			cv::line(histB_img, cv::Point(n, 256), cv::Point(n, 256 - 2560 * histB[256 - n] / ((img.cols) * (img.rows))), cv::Scalar(200, 0, 0), 1, 8);
			cv::line(histG_img, cv::Point(n, 256), cv::Point(n, 256 - 2560 * histG[256 - n] / ((img.cols) * (img.rows))), cv::Scalar(0, 200, 0), 1, 8);
			cv::line(histR_img, cv::Point(n, 256), cv::Point(n, 256 - 2560 * histR[256 - n] / ((img.cols) * (img.rows))), cv::Scalar(0, 0, 200), 1, 8);
		}
		//cv::namedWindow("hist", CV_WINDOW_AUTOSIZE | CV_WINDOW_FREERATIO);
		if (waitKey(1) == 's'){
			criteria = radius;
		}
		if (radius == 0){
			cv::putText(img, "not found face", cv::Point(50, 50), face[4] | face[8], 1, cv::Scalar(200, 100, 255), 0.5, CV_AA);
		}
		else if (criteria == 0){
			// 画像，テキスト，位置（左下），フォント，スケール，色，線太さ，種類
			cv::putText(img, "pless 's' key away one meters", cv::Point(50, 50), face[4] | face[8], 0.8, cv::Scalar(100, 255, 200), 0.5, CV_AA);
		}
		else{
			cv::putText(img, "distance = " + to_string(criteria / radius) +"m", cv::Point(50, 50), face[4] | face[8], 1, cv::Scalar(255, 200, 100), 0.5, CV_AA);
		}
		//cout << histB[100] << "," << histG[100] << "," << histR[100] << "\n";
		imshow("sample", img);
		cv::imshow("blue hist", histB_img);
		cv::imshow("green hist", histG_img);
		cv::imshow("red hist", histR_img);

		//cvSetMouseCallback("sample", Mouse);
	}
	return(0);
}