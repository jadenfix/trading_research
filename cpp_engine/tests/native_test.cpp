#include <cstddef>
#include <cmath>
#include <limits>
extern "C" int research_ma(const double*,std::size_t,std::size_t,std::size_t,int*);
int main(){
 double p[]={100,101,102,103,104,105,106}; int out[7];
 if(research_ma(p,7,2,4,out)!=0 || out[3]!=0 || out[4]!=1) return 1;
 p[6]=50; if(research_ma(p,7,2,4,out)!=0 || out[6]!=1) return 2;
 p[2]=std::numeric_limits<double>::quiet_NaN();
 if(research_ma(p,7,2,4,out)!=1) return 3;
 if(research_ma(nullptr,7,2,4,out)!=1) return 4;
 return 0;
}
