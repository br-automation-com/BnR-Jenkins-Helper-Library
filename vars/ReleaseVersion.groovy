def call(Map config = [:]) {
    def fullVersion = Version(config);
    return fullVersion.substring(0, fullVersion.lastIndexOf('.'));
}
