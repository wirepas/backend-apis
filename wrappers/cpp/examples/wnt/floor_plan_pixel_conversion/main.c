/* Copyright 2020 Wirepas Ltd licensed under Apache License, Version 2.0
 *
 * See file LICENSE for full license details.
 *
 */
#include <math.h>
#include <stdio.h>
#include <string.h>

#ifndef M_PI
    #define M_PI acos(-1.0)
#endif
#define MATRIX_ITEM_COUNT (3 * 3)

/** Structure to hold point in 2d */
typedef struct
{
    double x;
    double y;
} point_2d_t;

/** Structure to hold point in 3d */
typedef struct
{
    double x;
    double y;
    double z;
} point_3d_t;

/** Structure to hold WGS84 coordinates */
typedef struct
{
    double latitude;
    double longitude;
    double altitude;
} location_t;

/**
 * \brief   Function to convert degrees to radians
 * \param   deg
 *          Value in degrees
 * \return  Value in radians
 */
static double deg_to_rad(double deg)
{
    return deg * M_PI / 180.0;
}

/**
 * \brief   Function to convert radians to degrees
 * \param   rad
 *          Value in radians
 * \return  Value in degrees
 */
static double rad_to_deg(double rad)
{
    return rad * 180.0 / M_PI;
}

/**
 * \brief   Function to convert WGS84 coordinates to ECEF coordinates
 * \param   location
 *          WGS84 coordinates
 * \return  ECEF coordinates
 */
static point_3d_t wgs82_to_ecef(location_t location)
{
    const double a = 6378137.0;
    const double finv = 298.257223563;

    const double f = 1.0 / finv;
    double e2 = 1.0 - pow(1.0 - f, 2);

    double latitude_rad = deg_to_rad(location.latitude);
    double longitude_rad = deg_to_rad(location.longitude);

    double v = a / sqrt(1.0 - e2 * sin(latitude_rad) * sin(latitude_rad));

    point_3d_t point_ecef;

    point_ecef.x = (v + location.altitude) * cos(latitude_rad) * cos(longitude_rad);
    point_ecef.y = (v + location.altitude) * cos(latitude_rad) * sin(longitude_rad);
    point_ecef.z = (v * (1.0 - e2) + location.altitude) * sin(latitude_rad);

    return point_ecef;
}

/**
 * \brief   Function to convert ECEF coordinates to WGS84 coordinates
 * \param   ecef_point
 *          ECEF coordinates
 * \return  WGS84 coordinates
 */
static location_t ecef_to_wgs84(point_3d_t ecef_point)
{
    const double a = 6378137.0;
    const double finv = 298.257223563;

    const double f = 1.0 / finv;
    double e2 = 1.0 - pow(1.0 - f, 2);

    double elat = pow(10, -12);
    double eht = pow(10, -5);

    double p = sqrt(ecef_point.x * ecef_point.x + ecef_point.y * ecef_point.y);
    double lat = atan2(ecef_point.z, p * (1.0 - e2));
    double h = 0;
    double dh = 1;
    double dlat = 1;

    while (dlat > elat || dh > eht)
    {
        double lat0 = lat;
        double h0 = h;
        double v = a / sqrt(1.0 - e2 * sin(lat) * sin(lat));

        h = p / cos(lat) - v;
        lat = atan2(ecef_point.z, p * (1.0 - e2 * v / (v + h)));
        dlat = fabs(lat - lat0);
        dh = fabs(h - h0);
    }

    double lon = atan2(ecef_point.y, ecef_point.x);

    location_t location;

    location.latitude = rad_to_deg(lat);
    location.longitude = rad_to_deg(lon);
    location.altitude = h;

    return location;
}

/**
 * \brief   Function to convert floor plan pixel coordinates to WGS84 coordinates
 * \param   rotation_matrix
 *          Rotation matrix from WNT backend
 * \param   reverse_transformation_vector
 *          Offset vector from WNT backend
 * \param   scale_pixels_per_meter
 *          Scale from WNT backend
 * \param   pixel_position_vector
 *          Pixel coordinates to map to WGS84 coordinates
 * \return  WGS84 coordinates
 */
static location_t get_location(double *rotation_matrix, point_3d_t reverse_transformation_vector,
    double scale_pixels_per_meter, point_2d_t pixel_position_vector)
{
    double transposed_rotation_matrix[MATRIX_ITEM_COUNT] = { 0 };
    memcpy(transposed_rotation_matrix, rotation_matrix, sizeof(transposed_rotation_matrix));

    transposed_rotation_matrix[1] = rotation_matrix[3];
    transposed_rotation_matrix[2] = rotation_matrix[6];
    transposed_rotation_matrix[3] = rotation_matrix[1];
    transposed_rotation_matrix[5] = rotation_matrix[7];
    transposed_rotation_matrix[6] = rotation_matrix[2];
    transposed_rotation_matrix[7] = rotation_matrix[5];

    point_3d_t pixel_delta_vector;

    pixel_delta_vector.x =
        transposed_rotation_matrix[0] * pixel_position_vector.x +
        transposed_rotation_matrix[1] * pixel_position_vector.y;

    pixel_delta_vector.y =
        transposed_rotation_matrix[3] * pixel_position_vector.x +
        transposed_rotation_matrix[4] * pixel_position_vector.y;

    pixel_delta_vector.z =
        transposed_rotation_matrix[6] * pixel_position_vector.x +
        transposed_rotation_matrix[7] * pixel_position_vector.y;

    pixel_delta_vector.x /= scale_pixels_per_meter;
    pixel_delta_vector.y /= scale_pixels_per_meter;
    pixel_delta_vector.z /= scale_pixels_per_meter;

    point_3d_t point_ecef;
    point_ecef.x = pixel_delta_vector.x + reverse_transformation_vector.x;
    point_ecef.y = pixel_delta_vector.y + reverse_transformation_vector.y;
    point_ecef.z = pixel_delta_vector.z + reverse_transformation_vector.z;

    return ecef_to_wgs84(point_ecef);
}

/**
 * \brief   Function to convert WGS84 coordinates to floor plan pixel coordinates
 * \param   rotation_matrix
 *          Rotation matrix from WNT backend
 * \param   reverse_transformation_vector
 *          Offset vector from WNT backend
 * \param   scale_pixels_per_meter
 *          Scale from WNT backend
 * \param   location
 *          WGS84 coordinates to map to pixel coordinates
 * \return  Pixel coordinates
 */
static point_2d_t get_pixel_position(double *rotation_matrix, point_3d_t reverse_transformation_vector,
    double scale_pixels_per_meter, location_t location)
{
    point_3d_t point_ecef = wgs82_to_ecef(location);

    point_ecef.x -= reverse_transformation_vector.x;
    point_ecef.y -= reverse_transformation_vector.y;
    point_ecef.z -= reverse_transformation_vector.z;

    point_2d_t point_pixel;

    point_pixel.x =
        rotation_matrix[0] * point_ecef.x +
        rotation_matrix[1] * point_ecef.y +
        rotation_matrix[2] * point_ecef.z;

    point_pixel.y =
        rotation_matrix[3] * point_ecef.x +
        rotation_matrix[4] * point_ecef.y +
        rotation_matrix[5] * point_ecef.z;

    point_pixel.x *= scale_pixels_per_meter;
    point_pixel.y *= scale_pixels_per_meter;

    return point_pixel;
}

/**
 * \brief   Main entry point
 * \return  Return value
 */
int main()
{
    /** Example values from WNT backend start */
    double rotation_matrix[] = {
        0.7788987921717944, 0.5526683279974951, 0.296436149586675,
        0.579597627535213, -0.4538080052202482, -0.6768492332518167,
        -0.2395480363285678, 0.6990107392783551, -0.6737957588651434
        };

    point_3d_t offset_local_to_ecef;
    offset_local_to_ecef.x = 1530181.848984246;
    offset_local_to_ecef.y = -4465265.612122585;
    offset_local_to_ecef.z = 4275385.419786042;

    double pixels_per_meter = 35;
    /** Example values from WNT backend end */

    /** Pixel coordinates to convert to WGS84 coordinates */
    point_2d_t point_to_map;
    point_to_map.x = 230;
    point_to_map.y = 272;

    printf("Point to map. X:%.0lf Y:%.0lf\n", point_to_map.x, point_to_map.y);

    location_t location =
        get_location(rotation_matrix, offset_local_to_ecef, pixels_per_meter, point_to_map);

    printf("Calculated location. Latitude:%.6lf Longitude:%.6lf Altitude:%.2lf\n",
        location.latitude, location.longitude, location.altitude);

    /** Convert the calculated WGS84 coordinates back to pixel coordinates */
    point_2d_t point =
        get_pixel_position(rotation_matrix, offset_local_to_ecef, pixels_per_meter, location);

    printf("Calculated point. X:%.0lf Y:%.0lf\n", point.x, point.y);
    printf("Press any key to close\n");

    getchar();

    return 0;
}
