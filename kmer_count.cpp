#include <iostream>
#include <algorithm>
#include <valarray>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <iostream>
#include <algorithm>
#include <valarray>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <map>
#include <cassert>


#define MAX_LINE_LENGTH 1000
using namespace std;


int debug;

void show_version(char* name)
{
    printf("%s by Late Lee, version: 1.0\n", name);
}


void usage(char* name)
{
    show_version(name);

    printf("         -h,  --help           short help\n");
    printf("         -i,  --seq        show version\n");
    printf("         -n,  --kmer        show kmer number\n");
    printf("         -s,  --shift        show shift number\n");
}



template<typename T>
inline int equals(T a, T b){
	return a == b;
}



template<typename T>
void check(vector<T> &src, map<T,int> &dst)
{
	for (size_t i = 0; i < src.size(); ++i) {
		T checkStr = src[i];
		int flag = 0;
		for (size_t j = 0; j < i; ++j) {
			if (equals(checkStr, src[j])) {
				flag = 1;
				break;
			}
		}
		if (!flag) {
			int count = 1;
			for (size_t j = i + 1; j < src.size(); ++j) {
				if (equals(checkStr, src[j])){
					++count;
				}
			}
			dst.insert(pair<T, int>(checkStr, count));
		}
	}
}


vector<string> split_char(char* seq,float len,float shift)
{
    int l = len;	
    string s=seq;
    int s_length = s.length();
    string N = "N";

    std::vector<std::string> values;
    for(int i = 0; i < s_length-l+1; i=i+1+shift)
    {
    	    string::size_type idx;
	    string sn = s.substr(i,l);
            idx=sn.find(N);
	    if(idx == string::npos)
            {
	    	values.push_back(sn);
	    }
    }

    return values;
    
}


char complement(char n)
{
    switch(n)
    {
    case 'A':
        return 'T';
    case 'T':
        return 'A';
    case 'G':
        return 'C';
    case 'C':
        return 'G';
    }
    assert(false);
    return ' ';
}


string DNA_complement(string nuseq)
{
    string nucs = nuseq;
    transform(
        begin(nucs),
        end(nucs),
        begin(nucs),
        complement);
    reverse(nucs.begin(),nucs.end());
    return nucs;
}


int main(int argc, char *argv[])
{
    int i = 0;
    char* seq;
    char* number;
    char* shift;

    /* early check for debug and config parameter */

    for (i = 1; i < argc; i++)
    {
         if ((strcmp(argv[i], "-h")==0) || (strcmp(argv[i], "--help")==0))
         {
             usage(argv[i]);
         }
         if ((strcmp(argv[i], "-i")==0) || (strcmp(argv[i], "--seq")==0))
         {
	     seq=argv[i+1];

         }
	 if ((strcmp(argv[i], "-k")==0) || (strcmp(argv[i], "--kmer")==0))
       	 {
             number=argv[i+1];
	 
 	 }

	 if ((strcmp(argv[i], "-s")==0) || (strcmp(argv[i], "--shift")==0))
         {
             shift=argv[i+1];
         }

    }
    
    float num = atof(number);
    float st = atof(shift);
 

    std::vector<std::string> vs;
    vs = split_char(seq,num,st);

    //string
    //define map(key and value)    
    map<string, int> vsDst;
    check(vs, vsDst);
    //define map iterator
    map<string, int>::iterator it1;
    map<string, int>::iterator it2;
    

    for (it1 = vsDst.begin(); it1 != vsDst.end(); ++it1)
    {
	 for (it2 = vsDst.begin(); it2 != vsDst.end(); ++it2)
   	 {
		 if((*it1).first == DNA_complement((*it2).first))
		 {
			it1 = vsDst.find((*it1).first);
			it2 = vsDst.find(DNA_complement((*it2).first));
			//map get key(first) and value(second)			
			string name = it1->first;
			int val_1 = it1->second;
			int val_2 = it2->second;
			//cout << name << ":" << val_1 + val_2 << endl;
			vsDst.erase(DNA_complement((*it2).first));
			vsDst[(*it1).first] = val_1 + val_2;
		 } 
	 }

	//cout << (*it1).first << "," << (*it1).second << endl;
    }

    for (it1 = vsDst.begin(); it1 != vsDst.end(); ++it1)
    {
    	cout << (*it1).first << "," << (*it1).second << endl;
    }

  return 1;
} 
