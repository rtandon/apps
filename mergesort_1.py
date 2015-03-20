def mergeSort(alist,alist1):
    print("Splitting ",alist)
    if len(alist)>1:
        mid = len(alist)//2
        lefthalf = alist[:mid]
        righthalf = alist[mid:]

        mergeSort(lefthalf,alist1)
        mergeSort(righthalf,alist1)

        i=0
        j=0
        k=0
 
        print '<------alist 0------->'
        print alist
        print lefthalf
        print righthalf
        while i<len(lefthalf) and j<len(righthalf):
            if lefthalf[i]<righthalf[j]:
                alist1[k]=lefthalf[i]
                i=i+1
            else:
                alist1[k]=righthalf[j]
                j=j+1
            k=k+1
        print '<------alist 1------->'
        print alist1
        while i<len(lefthalf):
            alist1[k]=lefthalf[i]
            i=i+1
            k=k+1

        print '<------alist 2------->'
        print alist1
        while j<len(righthalf):
            alist1[k]=righthalf[j]
            j=j+1
            k=k+1
    print("Merging ",alist1)

#alist = [54,26,93,17,77,31,44,55,20]
alist = [54,26,93]
alist1 = [0,0,0]
mergeSort(alist,alist1)
print(alist)
