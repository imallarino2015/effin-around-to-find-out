#ifndef BMP_H
#define BMP_H

#include<iostream>
#include<fstream>
#include <string>

#include <GL/gl.h>

class Bitmap{
	private:
		char *label = 0;
		uint32_t imageBytes;
		uint16_t *reserved = 0;
		uint32_t pixelArrayOffset;
		uint32_t headerSize;
		uint32_t width;
		uint32_t height;
		uint16_t nPlaneColors;
		uint16_t colorDepth;
		uint32_t compressionMethod;
		uint32_t imageSize;
		uint32_t horizontalResolution;
		uint32_t verticalResolution;
		uint32_t nColors;
		uint32_t nColorsUsed;
		uint8_t ***data = 0;
	public:
		Bitmap(std::string);
		Bitmap(const Bitmap&);
		virtual ~Bitmap();

		void operator=(const Bitmap&);

		void open(std::string);
		void save(std::string);

		uint32_t getWidth();
		uint32_t getHeight();
		uint8_t getColor(unsigned x, unsigned y, unsigned byte);
		void setColor(unsigned x, unsigned y, unsigned byte, uint8_t val);

		void printHeader();
		void print();

		void makeGrayscale();
		void applyKernel();
		void resize(uint32_t, uint32_t);
		void clear();
};

int getBytes(std::ifstream& f, int nBytes=1){
	int n = 0;
	for(int a=0;a<nBytes;a++)
		n += f.get() << 8 * a;
	return n;
}

template<class t>
void writeBytes(std::ofstream& f, t val){
	unsigned nBytes=sizeof(val);
	for(unsigned a=0;a<nBytes;a++){
		uint8_t writeVal=val%256;
		val>>=8;
		f<<writeVal;
	}
}

Bitmap::Bitmap(std::string filePath){
	this->open(filePath);
}

Bitmap::Bitmap(const Bitmap& bmp){
	this->operator=(bmp);
}

Bitmap::~Bitmap(){
	this->clear();
}

void Bitmap::operator=(const Bitmap& bmp){
	this->label = new char[2]{bmp.label[0], bmp.label[1]};
	this->imageBytes = bmp.imageBytes;
	this->reserved = new uint16_t[2]{bmp.reserved[0], bmp.reserved[1]};
	this->pixelArrayOffset = bmp.pixelArrayOffset;
	this->headerSize = bmp.headerSize;
	this->width = bmp.width;
	this->height = bmp.height;
	this->nPlaneColors = bmp.nPlaneColors;
	this->colorDepth = bmp.colorDepth;
	this->compressionMethod = bmp.compressionMethod;
	this->imageSize = bmp.imageSize;
	this->horizontalResolution = bmp.horizontalResolution;
	this->verticalResolution = bmp.verticalResolution;
	this->nColors = bmp.nColors;
	this->nColorsUsed = bmp.nColorsUsed;

	this->data = new uint8_t**[height];
	for(unsigned y = 0; y < height; y++){
		this->data[y] = new uint8_t*[width];
		for(unsigned x=0;x<width;x++){
			this->data[y][x] = new uint8_t[colorDepth/sizeof(data[y][x])];
			for(unsigned c=0;c<colorDepth/sizeof(data[y][x]);c++){
				this->data[y][x][c] = bmp.data[y][x][c];
			}
		}
	}
}

void Bitmap::open(std::string filePath){
	this->clear();
	std::ifstream f = std::ifstream(filePath, std::fstream::binary);
	if(!f.is_open())
		throw std::invalid_argument("File does not exist");

	this->label = new char[2]{getBytes(f, 1), getBytes(f, 1)};
	this->imageBytes = getBytes(f, 4);
	this->reserved = new uint16_t[2]{getBytes(f, 2), getBytes(f, 2)};
	this->pixelArrayOffset = getBytes(f, 4);
	this->headerSize = getBytes(f, 4);
	this->width = getBytes(f, 4);
	this->height = getBytes(f, 4);
	this->nPlaneColors = getBytes(f, 2);
	this->colorDepth = getBytes(f, 2);
	this->compressionMethod = getBytes(f, 4);
	this->imageSize = getBytes(f, 4);
	this->horizontalResolution = getBytes(f, 4);
	this->verticalResolution = getBytes(f, 4);
	this->nColors = getBytes(f, 4);
	this->nColorsUsed = getBytes(f, 4);

	this->data = new uint8_t**[height];
	for(unsigned y = 0; y < height; y++){
		this->data[y] = new uint8_t*[width];
		for(unsigned x=0;x<width;x++){
			this->data[y][x] = new uint8_t[colorDepth/sizeof(data[y][x])];
			for(unsigned c=0;c<colorDepth/sizeof(data[y][x]);c++){
				this->data[y][x][c] = getBytes(f);
			}
		}
		getBytes(f, (4 - (width * colorDepth / 8) % 4) % 4);
	}
	f.close();
}

void Bitmap::save(std::string filePath){
	std::ofstream f = std::ofstream(filePath, std::fstream::binary);

	writeBytes(f, this->label[0]);
	writeBytes(f, this->label[1]);
	writeBytes(f, this->imageBytes);
	writeBytes(f, this->reserved[0]);
	writeBytes(f, this->reserved[1]);
	writeBytes(f, this->pixelArrayOffset);
	writeBytes(f, this->headerSize);
	writeBytes(f, this->width);
	writeBytes(f, this->height);
	writeBytes(f, this->nPlaneColors);
	writeBytes(f, this->colorDepth);
	writeBytes(f, this->compressionMethod);
	writeBytes(f, this->imageSize);
	writeBytes(f, this->horizontalResolution);
	writeBytes(f, this->verticalResolution);
	writeBytes(f, this->nColors);
	writeBytes(f, this->nColorsUsed);

	for(unsigned y=0;y<height;y++){
		for(unsigned x=0;x<width;x++){
			for(unsigned c=0;c<colorDepth/sizeof(data[y][x]);c++){
				f<<this->data[y][x][c];
			}
		}
		for(unsigned i=0;i<(4-(width*colorDepth/8)%4)%4;i++){
			f<<0;
		}
	}

	f.close();
}

uint32_t Bitmap::getWidth(){
	return this->width;
}

uint32_t Bitmap::getHeight(){
	return this->height;
}

uint8_t Bitmap::getColor(unsigned x, unsigned y, unsigned c){
	return this->data[this->height - 1 - y][x][this->colorDepth / 8 - 1 - c];
}

void Bitmap::setColor(unsigned x, unsigned y, unsigned byte, uint8_t val){
	this->data[this->height - 1 - y][x][this->colorDepth / 8 - 1 - byte] = val;
}

void Bitmap::printHeader(){
    std::cout<<"Label: "<<this->label[0]<<this->label[1]<<std::endl
		<<"Image bytes: "<<this->imageBytes<<std::endl
		<<"Reserved: "<<this->reserved[0]<<", "<<reserved[1]<<std::endl
		<<"Pixel offset: "<<this->pixelArrayOffset<<std::endl
		<<"Header size: "<<this->headerSize<<std::endl
		<<"Width: "<<this->width<<std::endl
		<<"Height: "<<this->height<<std::endl
		<<"Number of plane colors: "<<this->nPlaneColors<<std::endl
		<<"Color depth: "<<this->colorDepth<<" bits"<<std::endl
		<<"Compression method: "<<this->compressionMethod<<std::endl
		<<"Image size: "<<this->imageSize<<std::endl
		<<"Horizontal resolution: "<<this->horizontalResolution<<std::endl
		<<"Vertical resolution: "<<this->verticalResolution<<std::endl
		<<"Number of colors: "<<this->nColors<<std::endl
		<<"Number of colors used: "<<this->nColorsUsed<<std::endl;
}

void Bitmap::print(){
	for(unsigned y=0;y<this->height;y++){
		for(unsigned x=0;x<this->width;x++){
			std::cout<<"("<<x<<", "<<y<<"): ";
			for(unsigned c=0;c<this->colorDepth / 8;c++){
				std::cout<<(unsigned int8_t)this -> getColor(x, y, c)
					<<(c<this->colorDepth / 8 - 1?", ":"");
			}
			std::cout<<std::endl;
		}
	}
}

void Bitmap::makeGrayscale(){
	for(unsigned y=0;y<this->height;y++){
		for(unsigned x=0;x<this->width;x++){
			uint8_t val=(
				this->getColor(x, y, 0) * 0.2989 +
				this->getColor(x, y, 1) * 0.5870 +
				this->getColor(x, y, 2) * 0.1140
			);
			this->setColor(x, y, 0, val);
			this->setColor(x, y, 1, val);
			this->setColor(x, y, 2, val);
		}
	}
}

void Bitmap::applyKernel(){} ///Unimplemented

void Bitmap::resize(uint32_t width, uint32_t height){	///TODO

	this->width = width;
	this->height = height;
	this->imageSize = this->width * this->height * this->colorDepth / 8;
	this->imageBytes = this->imageSize + this->pixelArrayOffset;
}

void Bitmap::clear(){
	if(this->label){
		delete[] this->label;
		this->label = 0;
	}

	if(this->reserved){
		delete[] this->reserved;
		this->reserved = 0;
	}

	if(this->data){
		for(unsigned y=0;y<this->height;y++){
			for(unsigned x=0;x<this->width;x++){
				delete[] this->data[y][x];
				this->data[y][x] = 0;
			}
			delete[] this->data[y];
			this->data[y] = 0;
		}
		delete[] this->data;
		this->data = 0;
	}
}

#endif // BMP_H
