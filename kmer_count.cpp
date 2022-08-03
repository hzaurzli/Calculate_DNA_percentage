#include <iostream>
#include <valarray>
#include <vector>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <algorithm>
#include <map>
#include <cassert>


#define MAX_LINE_LENGTH 1000
using namespace std;
using std::cout; 
using std::cin;
using std::endl; 
using std::string;
using std::vector;


int debug;

void show_version(char* names)
{
    printf("%s by Small runze, version: 1.0\n", names);
}


void usage(char* names)
{
    show_version(names);

    printf("         -h,  --help       short help\n");
    printf("         -i,  --seq        show sequence\n");
    printf("         -f,  --file       show fasta file\n");
    printf("         -k,  --kmer       show kmer number\n");
    printf("         -s,  --shift      show shift number\n");
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


map<string, int> split_char(char* seq,float len,float shift)
{
  int l = len;	
  string s=seq;
  int s_length = s.length();
  string N = "N";
  
  std::map<string, int> mymap;
  for(int i = 0; i < s_length-l+1; i=i+1+shift)
  {
    string::size_type idx;
    string sn = s.substr(i,l);
    idx=sn.find(N);
    if(idx == string::npos)
    {   
      string csn = DNA_complement(sn);
      if(sn < csn)
      {
        if(mymap.find(sn) == mymap.end())
        {
          mymap[sn] = 1;
        }
        else{
          int val = mymap[sn];
          mymap[sn] = val + 1;
        }
      }
      if(sn == csn)
      {
        if(mymap.find(sn) == mymap.end())
        {
          mymap[sn] = 1;
        }
        else{
          int val = mymap[sn];
          mymap[sn] = val + 1;
        }
      }
      if(sn > csn)
      {
        if(mymap.find(csn) == mymap.end())
        {
          mymap[csn] = 1;
        }
        else{
          int val = mymap[csn];
          mymap[csn] = val + 1;
        }
      }
    }
  }
  return mymap;
}


map<string, int> split_char_all(char* seq,float len,float shift,map<string, int> vs)
{
  int l = len;	
  string s=seq;
  int s_length = s.length();
  string N = "N";
  
  for(int i = 0; i < s_length-l+1; i=i+1+shift)
  {
    string::size_type idx;
    string sn = s.substr(i,l);
    idx=sn.find(N);
    if(idx == string::npos)
    {   
      string csn = DNA_complement(sn);
      if(sn < csn)
      {
        if(vs.find(sn) == vs.end())
        {
          vs[sn] = 1;
        }
        else{
          int val = vs[sn];
          vs[sn] = val + 1;
        }
      }
      if(sn == csn)
      {
        if(vs.find(sn) == vs.end())
        {
          vs[sn] = 1;
        }
        else{
          int val = vs[sn];
          vs[sn] = val + 1;
        }
      }
      if(sn > csn)
      {
        if(vs.find(csn) == vs.end())
        {
          vs[csn] = 1;
        }
        else{
          int val = vs[csn];
          vs[csn] = val + 1;
        }
      }
    }
  }
  
  return vs;
}


int main(int argc, char *argv[])
{
    FILE *fi;
    int i = 0;
    char* seq;
    char* number;
    char* shift;
    char* path;
    char* nn = (char*)("no");

    /* early check for debug and config parameter */
    map<string, char*> param = 
    {
      {"-i",(char*)("no")}, 
      {"-f",(char*)("no")}, 
      {"-k",(char*)("no")},
      {"-s",(char*)("no")},
    };
    
    for (i = 1; i < argc; i++)
    {
         if ((strcmp(argv[i], "-h")==0) || (strcmp(argv[i], "--help")==0))
         {
             usage(argv[i]);
	           return 0;
         }
         if ((strcmp(argv[i], "-i")==0) || (strcmp(argv[i], "--seq")==0))
         {
	           seq=argv[i+1];
             param.find("-i")->second = seq;
         }
         if ((strcmp(argv[i], "-f")==0) || (strcmp(argv[i], "--file")==0))
         {
             path=argv[i+1];
             param.find("-f")->second = path;
         } 
	       if ((strcmp(argv[i], "-k")==0) || (strcmp(argv[i], "--kmer")==0))
       	 {
             number=argv[i+1];
	           param.find("-k")->second = number;
	           
 	       }
	       if ((strcmp(argv[i], "-s")==0) || (strcmp(argv[i], "--shift")==0))
         {
             shift=argv[i+1];
	           param.find("-s")->second = shift;
         }
    }
    
    //cout<<param["-s"]<<endl;
    
    char* sq = param["-i"];
    char* sf = param["-f"];
    char* sk = param["-k"];
    char* st = param["-s"];
    
    if(!strcmp(sq, nn)==0){
      if(!(strcmp(sk, nn)==0))
      {
        if(!(strcmp(st, nn)==0))
        {
          float skf = atof(sk);
          float stf = atof(st);
          
          //string
          //define map(key and value)
          map<string, int> vsDst;
          vsDst = split_char(sq,skf,stf);
          
          map<string, int>::iterator it1;
          
          for (it1 = vsDst.begin(); it1 != vsDst.end(); ++it1)
          {  
            cout << (*it1).first << "," << (*it1).second << endl;
          }
        }
        else{
          float skf = atof(sk);
          float stf = 0;
          
          //string
          //define map(key and value)
          map<string, int> vsDst;
          vsDst = split_char(sq,skf,stf);
          
          map<string, int>::iterator it1;
          
          for (it1 = vsDst.begin(); it1 != vsDst.end(); ++it1)
          {  
            cout << (*it1).first << "," << (*it1).second << endl;
          }
        }
      }
      else{
        if(!(strcmp(st, nn)==0))
        {
          float skf = 5;
          float stf = atof(st);
          
          //string
          //define map(key and value)
          map<string, int> vsDst;
          vsDst = split_char(sq,skf,stf);
          
          map<string, int>::iterator it1;
          
          for (it1 = vsDst.begin(); it1 != vsDst.end(); ++it1)
          {  
            cout << (*it1).first << "," << (*it1).second << endl;
          }
        }
        else{
          float skf = 5;
          float stf = 0;
          
          //string
          //define map(key and value)
          map<string, int> vsDst;
          vsDst = split_char(sq,skf,stf);
          
          map<string, int>::iterator it1;
          
          for (it1 = vsDst.begin(); it1 != vsDst.end(); ++it1)
          {  
            cout << (*it1).first << "," << (*it1).second << endl;
          }
        }
      }
    }
    
    if(!(strcmp(sf, nn)==0)){
      char line[MAX_LINE_LENGTH];
      fi = fopen(sf, "r");
      if(!(strcmp(sk, nn)==0))
      {
        if(!(strcmp(st, nn)==0))
        {
          int count = 1;
          float skf = atof(sk);
          float stf = atof(st);
          
          map<string, int> vsDst;
          while(fgets(line, MAX_LINE_LENGTH, fi) != NULL ){
            if(count%2==0){
              char* str = (char*)(line);
              str[strlen(str)-1]=0;
              vsDst = split_char_all(str,skf,stf,vsDst);
            }
            count++;
          }
          
          //define map iterator
          map<string, int>::iterator it1;
          for (it1 = vsDst.begin(); it1 != vsDst.end(); ++it1)
          {  
            cout << (*it1).first << "," << (*it1).second << endl;
          }
        }
        else{
          int count = 1;
          float skf = atof(sk);
          float stf = 0;
          
          
          map<string, int> vsDst;
          while(fgets(line, MAX_LINE_LENGTH, fi) != NULL ){
            if(count%2==0){
              char* str = (char*)(line);
              str[strlen(str)-1]=0;
              vsDst = split_char_all(str,skf,stf,vsDst);
            }
            count++;
          }
          
          //define map iterator
          map<string, int>::iterator it1;
          for (it1 = vsDst.begin(); it1 != vsDst.end(); ++it1)
          {  
            cout << (*it1).first << "," << (*it1).second << endl;
          }
        }
      }
      else{
        if(!(strcmp(st, nn)==0))
        {
          int count = 1;
          float skf = 5;
          float stf = atof(st);
          map<string, int> vsDst;
          while(fgets(line, MAX_LINE_LENGTH, fi) != NULL ){
            if(count%2==0){
              char* str = (char*)(line);
              str[strlen(str)-1]=0;
              vsDst = split_char_all(str,skf,stf,vsDst);
            }
            count++;
          }
          
          //define map iterator
          map<string, int>::iterator it1;
          for (it1 = vsDst.begin(); it1 != vsDst.end(); ++it1)
          {  
            cout << (*it1).first << "," << (*it1).second << endl;
          }
        }
        else{
          int count = 1;
          float skf = 5;
          float stf = 0;
          
          
          map<string, int> vsDst;
          while(fgets(line, MAX_LINE_LENGTH, fi) != NULL ){
            if(count%2==0){
              char* str = (char*)(line);
              str[strlen(str)-1]=0;
              vsDst = split_char_all(str,skf,stf,vsDst);
            }
            count++;
          }
          
          //define map iterator
          map<string, int>::iterator it1;
          for (it1 = vsDst.begin(); it1 != vsDst.end(); ++it1)
          {  
            cout << (*it1).first << "," << (*it1).second << endl;
          }
        }
      }
      return 0;
    }
    
    if(strcmp(sq, nn)==0 && strcmp(sf, nn)==0){
      printf("Please add correct paramters,-f or -i!\n");
      return 0;
    }
    return 1;
} 
      