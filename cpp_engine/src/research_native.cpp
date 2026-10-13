#include <cmath>
#include <cstddef>
#if defined(_WIN32)
#define API __declspec(dllexport)
#else
#define API __attribute__((visibility("default")))
#endif
// Positions at t use only prices through t-1; return status1 for invalid input.
extern "C" API int research_ma(const double* prices, std::size_t n,
                               std::size_t fast, std::size_t slow, int* positions) {
    if (!prices || !positions || fast == 0 || fast >= slow || n < slow + 1) return 1;
    for (std::size_t i=0;i<n;++i) if (!std::isfinite(prices[i]) || prices[i]<=0) return 1;
    for (std::size_t t=0;t<n;++t) {
        positions[t]=0;
        if (t<slow) continue;
        double a=0,b=0;
        for(std::size_t i=t-fast;i<t;++i) a+=prices[i];
        for(std::size_t i=t-slow;i<t;++i) b+=prices[i];
        positions[t]=(a/fast>b/slow)?1:((a/fast<b/slow)?-1:0);
    }
    return 0;
}
