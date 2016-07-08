% Get the pixel centers in search radius from lat lon point
function MODISpixelCenters_unh(filename,lat_point,lon_point,searchRadius,name)
% INPUTS
% filename - a filename for a MOD09GA hdf file within which the lat/lon
% point is
% lat_point - latitude
% lon_point - longitude
% searchRadius - in meters
% name - a name for the region (used input text file)
% OUTPUTS
% ----writes a text file with locations for lat - lon points that are
% centers of MODIS pixels
% Example: 
filename='/Users/ulyananadiahorodyskyj/Desktop/MOD09GA.A2016038.h15v02.005.2016040115606.hdf';
lat_point=66.9039306;
lon_point=-65.3260472;
searchRadius=5000;
name='baffin7_new';

% Get referencing information
[pstruct, ~, Rmap500m, ~, size500m]=makeSinusoidProj(filename);

% Get pixel centers and convert to lat lon
[x,y] = pixcenters(Rmap500m, size500m(1), size500m(2),'makegrid');
[lat,lon] = minvtran(pstruct,x,y);

% Convert lat/lon of area of interest to sinusoidal
[xp1,yp1] = mfwdtran(pstruct,lat_point,lon_point);

% Distance away from study area for every pixel
sz1=size500m(1);
sz2=size500m(2);
d=NaN(sz1,sz2);
parfor n=1:sz1
    for m=1:sz2
        d(n,m)=sqrt((yp1-y(n,m))^2+(xp1-x(n,m))^2);
    end
end

%Subset 1 of pixels w/in searchRadius
mask1=d<searchRadius;

% Linear index (instead of i,j index)
indxlinear1=find(mask1);

% Find lat/lon of the pixels within searchRadius
lat_P=lat(indxlinear1);
lon_P=lon(indxlinear1);

% Write in text file
dlmwrite(['AOI_' name '_lat' ...
    num2str(roundn(lat_point,-2)) '_lon' num2str(roundn(lon_point,-2)) '.txt'],...
[lat_P lon_P],'precision',12)