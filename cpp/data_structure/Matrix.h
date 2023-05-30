#ifndef MATRIX_H
#define MATRIX_H

#include <string>


class Matrix{
        uint32_t width = 0;
        uint32_t height = 0;
        float** matrix = 0;

    public:
        Matrix(uint32_t width=0, uint32_t height=0, float initVal=0){
            resize(width, height);

            for(unsigned y=0; y<this->height; y++)
                for(unsigned x=0; x<this->width; x++)
                    this->matrix[y][x] = initVal;
        }
        Matrix(const Matrix& other){
            resize(other.width, other.height);

            for(unsigned y=0; y<this->height; y++)
                for(unsigned x=0; x<this->width; x++)
                    this->matrix[y][x] = other.matrix[y][x];
        }
        //TODO: Matrix from array
        Matrix(float** vals){}

        Matrix cross(const Matrix& other){
            if (this->height != other.width)
                throw("Mismatching matrix dimensions; Left matrix height must match right matrix width.");

            Matrix retMat = Matrix(this->width, other.height);

            for(unsigned y=0;y<other.height;y++)
                for(unsigned x=0;x<this->width;x++){
                    float total = 0;
                    for(unsigned i=0;i<this->height;i++)
                        total += this->matrix[i][x] * other.matrix[y][i];
                    retMat.matrix[y][x] = total;
                }

            return retMat;
        }
        Matrix transpose(){
            Matrix retMat = Matrix(this->height, this->width);

            for(unsigned y=0; y<this->height; y++)
                for(unsigned x=0; x<this->width; x++)
                    retMat.matrix[x][y] = this->matrix[y][x];

            return retMat;
        }

        std::string to_string(){
            std::string retStr = "";

            for(unsigned y=0; y<this->height; y++){
                for(unsigned x=0; x<this->width; x++)
                    retStr += std::to_string(this->matrix[y][x]) + "\t";
                retStr += "\n";
            }

            return retStr;
        }
        std::string shape(){
            return std::to_string(this->width) + " x " + std::to_string(this->height);
        }

        void apply_inPlace(auto fn){
            for(unsigned y=0;y<this->height;y++)
                for(unsigned x=0;x<this->width;x++)
                    this->matrix[y][x] = fn(matrix[y][x]);
        }
        Matrix apply_return(auto fn){
            Matrix retMat = Matrix(this->width, this->height);
            for(unsigned y=0;y<this->height;y++)
                for(unsigned x=0;x<this->width;x++)
                    retMat.matrix[y][x] = fn(matrix[y][x]);

            return retMat;
        }

        void operator=(const Matrix& other){
            resize(other.width, other.height);

            for(unsigned y=0; y<this->height; y++)
                for(unsigned x=0; x<this->width; x++)
                    this->matrix[y][x] = other.matrix[y][x];
        };

        void operator=(float val){apply_return([val](float x){return val;});}
        Matrix operator+(float val){return apply_return([val](float x){return x + val;});}
        Matrix operator-(float val){return apply_return([val](float x){return x - val;});}
        Matrix operator*(float val){return apply_return([val](float x){return x * val;});}
        Matrix operator/(float val){return apply_return([val](float x){return x / val;});}
        void operator+=(float val){apply_inPlace([val](float x){return x + val;});}
        void operator-=(float val){apply_inPlace([val](float x){return x - val;});}
        void operator*=(float val){apply_inPlace([val](float x){return x * val;});}
        void operator/=(float val){apply_inPlace([val](float x){return x / val;});}

        void clear(){
            if(matrix){
                for(unsigned y=0; y<this->height; y++){
                    delete[] this->matrix[y];
                    this->matrix[y] = 0;
                }
                delete[] this->matrix;
                this->matrix = 0;
            }
        }
        void resize(uint32_t width=0, uint32_t height=0){
            if(width != this->width || height != this->height){
                clear();

                this->width = width;
                this->height = height;

                this->matrix = new float*[this->height];
                for(unsigned y=0; y<this->height; y++){
                    this->matrix[y] = new float[this->width];
                    for(unsigned x=0; x<this->width; x++)
                        this->matrix[y][x] = 0;
                }
            }
        }

        ~Matrix(){
            clear();
        }
};

#endif // MATRIX_H
