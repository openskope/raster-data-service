const rest = require('rest');
const mime = require('rest/interceptor/mime');

const timeseriesServiceBase = 'http://localhost:8001/timeseries-service/api/v1';

const callRESTService =  rest.wrap(mime, { mime: 'application/json' } );

describe("When a GET request selects from a region exactly covering the northwest 2x2 pixel area in the uint16 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-123,45],
	    		        [-123,47],
	    		        [-121,47],
	    		        [-121,45],
	    		        [-123,45]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the average of four pixels in each band', async function() {
        expect(response.entity.values[0]).toBeCloseTo(105.5,3);
        expect(response.entity.values[1]).toBeCloseTo(205.5,3);
        expect(response.entity.values[2]).toBeCloseTo(305.5,3);
        expect(response.entity.values[3]).toBeCloseTo(405.5,3);
        expect(response.entity.values[4]).toBeCloseTo(505.5,3);
    });
    
    it ('The data column should comprise the average of four pixels in each band', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,105.500"					+ "\n" +
        		"1,205.500"					+ "\n" +
        		"2,305.500"					+ "\n" +
        		"3,405.500" 				+ "\n" +
        		"4,505.500" 				+ "\n"
		);
    });
});

describe("When a GET request selects from a region exactly covering the northwest 2x2 pixel area in the float32 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'float32_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-123,45],
	    		        [-123,43],
	    		        [-121,43],
	    		        [-121,45],
	    		        [-123,45]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the average of four pixels in each band', async function() {
        expect(response.entity.values[0]).toBeCloseTo(105.55,3);
        expect(response.entity.values[1]).toBeCloseTo(205.55,3);
        expect(response.entity.values[2]).toBeCloseTo(305.55,3);
        expect(response.entity.values[3]).toBeCloseTo(405.55,3);
        expect(response.entity.values[4]).toBeCloseTo(505.55,3);
    });
    
    it ('The data column should comprise the average of four pixels in each band', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, float32_variable, range -, range +"	+ "\n" +
        		"0,105.550,95.0000,116.100"					+ "\n" +
        		"1,205.550,185.000,226.100"					+ "\n" +
        		"2,305.550,275.000,336.100"					+ "\n" +
        		"3,405.550,365.000,446.100" 				+ "\n" +
        		"4,505.550,455.000,556.100" 				+ "\n"
		);
    });
});

describe("When a GET request selects from a region of zero area from the uint16 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-122.5,45.5],
	    		    	[-122.5,45.5],
	    		    	[-122.5,45.5],
	    		    	[-122.5,45.5],
	    		    	[-122.5,45.5],
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that longitude parameter is not present', async function() {
        expect(response.entity.message).toBe("The selected area does not overlap the region covered by the dataset");
    }); 
});

describe("When a GET request selects from a region of zero area from the float32 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'float32_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-122.5,45.5],
	    		    	[-122.5,45.5],
	    		    	[-122.5,45.5],
	    		    	[-122.5,45.5],
	    		    	[-122.5,45.5],
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that longitude parameter is not present', async function() {
        expect(response.entity.message).toBe("The selected area does not overlap the region covered by the dataset");
    }); 
});


describe("When a GET request selects from a 2x2 pixel region that intersects a 2x1 pixel region in the uint16 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
    		    	[-123,44],
    		        [-123,46],
    		        [-121,46],
    		        [-121,44],
    		        [-123,44]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the average of four pixels in each band', async function() {
        expect(response.entity.values[0]).toBeCloseTo(100.5,3);
        expect(response.entity.values[1]).toBeCloseTo(200.5,3);
        expect(response.entity.values[2]).toBeCloseTo(300.5,3);
        expect(response.entity.values[3]).toBeCloseTo(400.5,3);
        expect(response.entity.values[4]).toBeCloseTo(500.5,3);
    });
    
    it ('The data column should comprise the average of the two pixels intersection of polygon and dataset', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,100.500"					+ "\n" +
        		"1,200.500"					+ "\n" +
        		"2,300.500"					+ "\n" +
        		"3,400.500"					+ "\n" +
    			"4,500.500"					+ "\n"
		);
    });
});

describe("When a GET request selects from a 2x2 pixel region that intersects a 2x1 pixel region in the float32 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'float32_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
    		    	[-123,46],
    		        [-123,44],
    		        [-121,44],
    		        [-121,46],
    		        [-123,46]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the average of four pixels in each band', async function() {
        expect(response.entity.values[0]).toBeCloseTo(100.55,3);
        expect(response.entity.values[1]).toBeCloseTo(200.55,3);
        expect(response.entity.values[2]).toBeCloseTo(300.55,3);
        expect(response.entity.values[3]).toBeCloseTo(400.55,3);
        expect(response.entity.values[4]).toBeCloseTo(500.55,3);
    });
    
    it ('The data column should comprise the average of the two pixels intersection of polygon and dataset', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, float32_variable, range -, range +" + "\n" +  
        		"0,100.550,90.5000,110.600"					+ "\n" +
        		"1,200.550,180.500,220.600"					+ "\n" +
        		"2,300.550,270.500,330.600"					+ "\n" +
        		"3,400.550,360.500,440.600"					+ "\n" +
        		"4,500.550,450.500,550.600"					+ "\n"
		);
    });
});


describe("When a GET request selects a region just outside coverage of the uint16 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
    		    	[-124,45],
    		        [-124,43],
    		        [-123,43],
    		        [-123,45],
    		        [-123,45]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that longitude parameter is not present', async function() {
        expect(response.entity.message).toBe("The selected area does not overlap the region covered by the dataset");
    }); 
});

describe("When a GET request selects a region just outside coverage of the float32 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'float32_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
    		    	[-124,45],
    		        [-124,43],
    		        [-123,43],
    		        [-123,45],
    		        [-123,45]
    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that coordinates are outside dataset coverage', async function() {
        expect(response.entity.message).toBe("The selected area does not overlap the region covered by the dataset");
    });
});

describe("When a GET request selects a region well outside coverage of the float32 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'float32_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
    		    	[-104,37],
    		        [-104,35],
    		        [-103,35],
    		        [-103,37],
    		        [-103,37]
    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 400', async function() {
        expect(response.status.code).toBe(400);
    });
    
    it ('Error summary should be bad request', async function() {
        expect(response.entity.error).toBe("Bad Request");
    });

    it ('Error message should be that coordinates are outside dataset coverage', async function() {
        expect(response.entity.message).toBe("The selected area does not overlap the region covered by the dataset");
    });
});

describe("When a GET request selects exactly the top-left corner pixel of the uint16 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-123.0,45],
	    		        [-123.0,46],
	    		        [-122,46],
	    		        [-122,45],
	    		        [-123.0,45]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the values of the top-left pixels in each band', async function() {
        expect(response.entity.values[0]).toBeCloseTo(100.0,3);
        expect(response.entity.values[1]).toBeCloseTo(200.0,3);
        expect(response.entity.values[2]).toBeCloseTo(300.0,3);
        expect(response.entity.values[3]).toBeCloseTo(400.0,3);
        expect(response.entity.values[4]).toBeCloseTo(500.0,3);
    });
    
    it ('The data column should comprise the values of the top-left pixels in each band', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,100.000"					+ "\n" +
        		"1,200.000"					+ "\n" +
        		"2,300.000"					+ "\n" +
        		"3,400.000"					+ "\n" +
    			"4,500.000"					+ "\n"
		);
    });
});

describe("When a GET request selects exactly the top-left corner pixel of the float32 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'float32_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-123.0,45],
	    		        [-123.0,44],
	    		        [-122.0,44],
	    		        [-122.0,45],
	    		        [-123.0,45]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the values of the top-left pixels in each band', async function() {
        expect(response.entity.values[0]).toBeCloseTo(100.0,3);
        expect(response.entity.values[1]).toBeCloseTo(200.0,3);
        expect(response.entity.values[2]).toBeCloseTo(300.0,3);
        expect(response.entity.values[3]).toBeCloseTo(400.0,3);
        expect(response.entity.values[4]).toBeCloseTo(500.0,3);
    });
    
    it ('The data column should comprise the values of the top-left pixels in each band', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, float32_variable, range -, range +" + "\n" +
        		"0,100.000,90.0000,110.000" 				+ "\n" +
        		"1,200.000,180.000,220.000" 				+ "\n" +
        		"2,300.000,270.000,330.000" 				+ "\n" +
        		"3,400.000,360.000,440.000" 				+ "\n" +
        		"4,500.000,450.000,550.000"					+ "\n"
		);
    });
});


describe("When a GET request selects 1/4 of the top-left corner pixel of the uint16 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-123.0,45],
	    		        [-123.0,45.25],
	    		        [-122.75,45.25],
	    		        [-122.75,45.25],
	    		        [-123.0,45]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the values of the top-left pixels in each band', async function() {
        expect(response.entity.values[0]).toBeCloseTo(100.0,3);
        expect(response.entity.values[1]).toBeCloseTo(200.0,3);
        expect(response.entity.values[2]).toBeCloseTo(300.0,3);
        expect(response.entity.values[3]).toBeCloseTo(400.0,3);
        expect(response.entity.values[4]).toBeCloseTo(500.0,3);
    });
    
    it ('The data column should comprise the values of the top-left pixels in each band', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,100.000"					+ "\n" +
        		"1,200.000"					+ "\n" +
        		"2,300.000"					+ "\n" +
        		"3,400.000"					+ "\n" +
    			"4,500.000"					+ "\n"
		);
    });
});

describe("When a GET request selects 1/4 of the top-left corner pixel of the float32 variable", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'float32_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-123.0,45],
	    		        [-123.0,44.75],
	    		        [-122.75,44.75],
	    		        [-122.75,44.75],
	    		        [-123.0,45]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the values of the top-left pixels in each band', async function() {
        expect(response.entity.values[0]).toBeCloseTo(100.0,3);
        expect(response.entity.values[1]).toBeCloseTo(200.0,3);
        expect(response.entity.values[2]).toBeCloseTo(300.0,3);
        expect(response.entity.values[3]).toBeCloseTo(400.0,3);
        expect(response.entity.values[4]).toBeCloseTo(500.0,3);
    });
    
    it ('The data column should comprise the values of the top-left pixels in each band', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, float32_variable, range -, range +" + "\n" +
        		"0,100.000,90.0000,110.000" 				+ "\n" +
        		"1,200.000,180.000,220.000" 				+ "\n" +
        		"2,300.000,270.000,330.000" 				+ "\n" +
        		"3,400.000,360.000,440.000" 				+ "\n" +
        		"4,500.000,450.000,550.000"					+ "\n"
		);
    });
});



describe("When a GET request selects from a region exactly covering the 2x2 pixel area in southwest corner the dataset", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-123,48],
	    		        [-123,50],
	    		        [-121,50],
	    		        [-121,48],
	    		        [-123,48]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the average of four pixels in each band', async function() {
        expect(response.entity.values[0]).toBeCloseTo(135.5,3);
        expect(response.entity.values[1]).toBeCloseTo(235.5,3);
        expect(response.entity.values[2]).toBeCloseTo(335.5,3);
        expect(response.entity.values[3]).toBeCloseTo(435.5,3);
        expect(response.entity.values[4]).toBeCloseTo(535.5,3);
    });
    
    it ('The data column should comprise the average of four pixels in each band', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,135.500"					+ "\n" +
        		"1,235.500"					+ "\n" +
        		"2,335.500"					+ "\n" +
        		"3,435.500"					+ "\n" +
    			"4,535.500"					+ "\n"
		);
    });
});

describe("When a GET request selects from a region exactly covering the 2x2 pixel area in southeast corner of uint16 variable with one NODATA pixel in each band", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-120,48],
	    		        [-118,50],
	    		        [-120,50],
	    		        [-120,48],
	    		        [-118,48]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the average of four pixels in each band', async function() {
        expect(response.entity.values[0]).toBeCloseTo(140.0,3);
        expect(response.entity.values[1]).toBeCloseTo(240.0,3);
        expect(response.entity.values[2]).toBeCloseTo(340.0,3);
        expect(response.entity.values[3]).toBeCloseTo(440.0,3);
        expect(response.entity.values[4]).toBeCloseTo(540.0,3);
    });
    
    it ('The data column should comprise the average of four pixels in each band', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,140.000"				    + "\n" +
        		"1,240.000"				    + "\n" +
        		"2,340.000"				    + "\n" +
        		"3,440.000"				    + "\n" +
    			"4,540.000"				    + "\n"
		);
    });
});

describe("When a GET request selects from a region exactly covering the 2x2 pixel area in southeast corner of float32 variable with one NODATA pixel in each band", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'float32_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-120,42],
	    		        [-118,40],
	    		        [-120,40],
	    		        [-120,42],
	    		        [-118,42]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the average of four pixels in each band', async function() {
        expect(response.entity.values).toEqual([null, null, null, null, null]);
    });
    
    it ('The data column should comprise the average of four pixels in each band', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, float32_variable, range -, range +"	+ "\n" +
        		"0,,,"				    					+ "\n" +
        		"1,,,"				    					+ "\n" +
        		"2,,,"				    					+ "\n" +
        		"3,,,"				    					+ "\n" +
    			"4,,,"				    					+ "\n"
		);
    });
});


describe("When a GET request selects from a region exactly covering the 2x2 pixel area in uint16 variable with one NODATA pixel in 3rd band", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'uint16_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-120,47],
	    		        [-118,49],
	    		        [-120,49],
	    		        [-120,47],
	    		        [-118,47]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the average of four pixels in each band', async function() {
        expect(response.entity.values[0]).toBeCloseTo(126.667,3);
        expect(response.entity.values[1]).toBeCloseTo(226.667,3);
        expect(response.entity.values[2]).toBeCloseTo(328.000,3);
        expect(response.entity.values[3]).toBeCloseTo(426.667,3);
        expect(response.entity.values[4]).toBeCloseTo(526.667,3);
    });
    
    it ('The data column should comprise the average of four pixels in each band', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, uint16_variable"	+ "\n" +
        		"0,126.667"					+ "\n" +
        		"1,226.667"					+ "\n" +
        		"2,328.000"					+ "\n" +
        		"3,426.667"					+ "\n" +
    			"4,526.667"					+ "\n"
		);
    });
});


describe("When a GET request selects from a region exactly covering the 2x2 pixel area in southeast corner of float32 variable with two NODATA pixels in 3rd band", async () => {
    
	var response;
	
	beforeAll(async () => {
		response = await callRESTService({
		    method: 'POST',
		    path: timeseriesServiceBase + '/timeseries',
		    entity: {
		    	datasetId: 'annual_5x5x5_dataset',
		    	variableName: 'float32_variable',
		    	boundaryGeometry: {
    		    "type": "Polygon",
    		    "coordinates": [[
	    		    	[-120,44],
	    		        [-118,42],
	    		        [-120,42],
	    		        [-120,44],
	    		        [-118,44]
	    		    	]]
	    		},
	    		start: 0,
	    		end: 4
		    }
		});
    });

    it ('HTTP response status code should be 200 - success', async function() {
        expect(response.status.code).toBe(200);
    });
    
    it ('The array should comprise the average of four pixels in each band', async function() {
        expect(response.entity.values[0]).toBeCloseTo(118.850,3);
        expect(response.entity.values[1]).toBeCloseTo(218.850,3);
        expect(response.entity.values[2]).toBe(null);
        expect(response.entity.values[3]).toBeCloseTo(418.850,3);
        expect(response.entity.values[4]).toBeCloseTo(518.850,3);
    });
    
    it ('The data column should comprise the average of four pixels in each band', async function() {
        expect(response.entity.csv).toEqual( 
        		"index, float32_variable, range -, range +"	+ "\n" +
        		"0,118.850,107.000,130.700"					+ "\n" +
        		"1,218.850,197.000,240.700"					+ "\n" +
        		"2,,,"										+ "\n" +
        		"3,418.850,377.000,460.700"					+ "\n" +
        		"4,518.850,467.000,570.700"	 				+ "\n"
		);
    });
});

