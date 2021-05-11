import numpy as np

class TopoGraph:
    def __init__(self):
        pass

    def topograph_construction_pruning(self,V,X_extend,Boundary,Dis,alpha,epsilon):
        E,E_hat,gamma,count={},{},{},{}
        X_mid=[]
        for (i,j,ri,rj) in Boundary:
            E[(ri,rj)]=0
            E[(rj,ri)]=0
            E_hat[ri]=0
            E_hat[rj]=0
            gamma[(ri,rj)]=None
            count[(ri,rj)]=0
            X_mid.append( (X_extend[i,-3],X_extend[j,-3]) )

        if len(X_mid)==0:
            return E.copy(),E

        X_mid=np.array(X_mid).astype(np.int)
        # P_left=Dis.get_density(X_mid[:,0])
        # P_right=Dis.get_density(X_mid[:,1])
        # P_mid = (P_left+P_right)/2

        # P_mid = np.exp(-(np.linalg.norm(X_extend[X_mid[:,0],:-4]-X_extend[X_mid[:,1],:-4],axis=1)/2/np.sqrt(X_extend.shape[1]-4))**2)
        P_mid = Dis.get_midP(X_mid[:,0],X_mid[:,1])

        Used_Bound_P=[]
        for idx,(i,j,ri,rj) in enumerate(Boundary):
            if i in Used_Bound_P:
                continue
            if j in Used_Bound_P:
                continue
            Used_Bound_P.append(i)
            Used_Bound_P.append(j)

            if gamma[(ri,rj)] is None:
                P1,P2=X_extend[ri,-4],X_extend[rj,-4]
                gamma[(ri,rj)]=gamma[(rj,ri)]=min(P1/P2,P2/P1)**2#/max(P2,P1)**2
            
            s= (gamma[(ri,rj)]*(P_mid[idx])**2) #/ (len(V[ri])*len(V[rj]))
            count[(ri,rj)]+=1
            count[(rj,ri)]=count[(ri,rj)]
            E[(ri,rj)]+=s
            E[(rj,ri)]=E[(ri,rj)]

            if E[(ri,rj)]>E_hat[ri]:
                E_hat[ri]=E[(ri,rj)]

            if E[(ri,rj)]>E_hat[rj]:
                E_hat[rj]=E[(ri,rj)]

        E_raw=E.copy()
        for key,value in E.items():
            i,j=key[0],key[1]
            if value<=alpha*E_hat[i] or value<=alpha*E_hat[j]:
                E[(i,j)]=0
                E[(j,i)]=0
                
        weights = sorted([one for one in E.values() if one>0])
        threshold = weights[int(len(weights)*alpha)]

        for key,value in E.items():
            i,j=key[0],key[1]
            if value<=threshold:
                E[(i,j)]=0
                E[(j,i)]=0
        return E_raw,E