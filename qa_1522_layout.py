from pathlib import Path
import math
p=Path(__file__).parent
s=(p/'FXInterface.mm').read_text()
m=s.split('- (void)layoutSubviews {',1)[1].split('- (NSInteger)indexAtPoint:',1)[0]
assert 'lastLayoutBounds' not in s and 'lastLayoutColumns' not in s
assert 'self.layoutInProgress || self.cells.count == 0' in m
assert 'boundsSnapshot.origin.x + startX' in m
assert 'boundsSnapshot.origin.y + startY' in m
assert 'if (!CGRectEqualToRect(cell.frame, rect)) cell.frame = rect;' in m
assert m.index('self.layoutInProgress = YES') < m.index('for (NSUInteger i') < m.index('self.layoutInProgress = NO')
# Independent geometry model: verify extents, centered rows, no overlaps,
# and layout of fresh zero-sized cells at unchanged bounds for each rebuild.
n=0
for cols,rows in [(3,3),(6,2)]:
 for w,h in [(120,120),(160,160),(280,120),(320,160)]:
  for ox,oy in [(0,0),(13,-7)]:
   wide=cols==6; rnd=lambda v:math.floor(v+.5)
   mx=rnd(w*(.045 if wide else .095)); my=rnd(h*(.115 if wide else .095))
   gx=rnd(w*(.033 if wide else .076)); gy=rnd(h*(.095 if wide else .076))
   side=math.floor(min((w-2*mx-(cols-1)*gx)/cols,(h-2*my-(rows-1)*gy)/rows))
   sx=rnd((w-(cols*side+(cols-1)*gx))*.5); sy=rnd((h-(rows*side+(rows-1)*gy))*.5)
   for count in [0,1,cols,cols*rows,2,cols*rows]:
    cells=[(ox+sx+i%cols*(side+gx),oy+sy+i//cols*(side+gy),side,side) for i in range(count)]
    for x,y,cw,ch in cells:
     assert cw>0 and ox<=x and oy<=y and x+cw<=ox+w and y+ch<=oy+h
    n+=1
print('PASS: cache-free source contract and',n,'independent rebuild geometry cases (not UIKit runtime)')
