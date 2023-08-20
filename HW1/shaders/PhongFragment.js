const PhongFragmentShader = `
#extension GL_OES_standard_derivatives : enable 

precision mediump float;

varying vec3 shading_mode;
varying vec3 vertexColor;
varying vec3 fragPosition;
varying vec3 fragNormal;
varying vec3 lightLocations[3];
varying vec3 lightColors[3];
varying vec3 lightKdKsCDs[3];
varying float Ka_val;
varying float Kd_val;
varying float Ks_val;
varying float Cd_val;
varying vec3 ambient_lightColor;

varying vec3 fragcolor;   // for gouraud shading
varying vec3 mvVertex;
varying vec3 N;

void main(void) {
    vec3 LightDirection[3];
    for(int j=0; j<3; j++) {
        LightDirection[j] = normalize(lightLocations[j] - mvVertex);
    }

    vec3 V = -normalize(mvVertex);
    vec3 reflect[3];
    for(int j=0; j<3; j++) {
        reflect[j] = normalize(2. * dot(LightDirection[j], N) * N - LightDirection[j]);
    }

    // ambient
    vec3 ambient = ambient_lightColor * Ka_val * fragcolor;

    // diffusion
    vec3 diffuse = vec3(0.0, 0.0, 0.0);
    vec3 diffuse_cos;
    for(int j=0; j<3; j++) {
        diffuse_cos[j] = max(dot(N, LightDirection[j]), 0.0);
        diffuse += lightColors[j] * Kd_val * fragcolor * diffuse_cos[j];
    }

    
    // specular
    vec3 specular = vec3(0.0, 0.0, 0.0);
    vec3 specular_cos;
    for(int j=0; j<3; j++) {
        specular_cos[j] = pow(max(dot(V, LightDirection[j]), 0.0), Cd_val);
        specular += lightColors[j] * Ks_val * specular_cos[j];
    }

    vec3 phongColor = ambient + diffuse + specular;
    gl_FragColor = vec4(phongColor, 1.0);    
}
`;